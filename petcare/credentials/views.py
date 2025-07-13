from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User, Group
from django.contrib import messages, auth
from credentials.models import Customer, Doctor
from daycare.models import Booking
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from datetime import datetime
from django.core.files.storage import default_storage

# Create your views here.

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username = username, password = password)
        if user is not None:
            if user.is_staff == True:
                if user.is_superuser == True:
                    auth.login(request, user)
                    return redirect('admin_booking_list')
                else:
                    doctor = Doctor.objects.get(user=user)
                    if doctor.status == True:
                        auth.login(request, user)
                        return redirect('doctor_dashboard')
                    else:
                        return redirect('doctor_confirmation')
            else:
                auth.login(request, user)
                request.session['user_id'] = user.id
                return redirect('/')
        else:
            messages.info(request, "Enter valid credentials")
            return redirect('login')
    return render(request, 'login.html')

def customer_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        mail = request.POST['email']
        address = request.POST['address']
        profile_pic = request.FILES.get('profile_pic')
        phone = request.POST['phone']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, "Username already taken")
                return redirect("customer_register")
            elif User.objects.filter(email=mail).exists():
                messages.info(request, "Email already registered")
                return redirect("customer_register")
            else:
                user=User.objects.create_user(first_name=firstname, last_name=lastname, username=username, email=mail, password=password1)
                user.save()
                customer=Customer(user=user, address=address, phone=phone, profile_pic=profile_pic)
                customer.user=user
                customer.save()
                print("User saved")
                my_customer_group = Group.objects.get_or_create(name='CUSTOMER')
                my_customer_group[0].user_set.add(user)
                return redirect('login')
        else:
            messages.info(request, "Password doesn't match")
        
    return render(request, 'customer_register.html')

def logout(request):
    auth.logout(request)
    return redirect('/')

def doctor_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        mail = request.POST['email']
        specialisation = request.POST['specialisation']
        address = request.POST['address']
        profile_pic = request.FILES.get('profile_pic')
        phone = request.POST['phone']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, "Username already taken")
                return redirect("doctor_register")
            elif User.objects.filter(email=mail).exists():
                messages.info(request, "Email already registered")
                return redirect("doctor_register")
            else:
                user=User.objects.create_user(first_name=firstname, last_name=lastname, username=username, email=mail, password=password1, is_staff=True)
                user.save()
                doctor=Doctor(user=user, address=address, speacialisation=specialisation, phone=phone, profile_pic=profile_pic)
                doctor.user=user
                doctor.save()
                print("User saved")
                my_doctor_group = Group.objects.get_or_create(name='DOCTOR')
                my_doctor_group[0].user_set.add(user)
                return redirect('login')
        else:
            messages.info(request, "Password doesn't match")
        
    return render(request, 'doctor_register.html')

def booking_success(request):
    return render(request, 'booking_success.html')

def payment(request, payment_id):
    if request.method == 'POST':
        booking = Booking.objects.get(id=payment_id)
        booking.payment_status = True
        booking.save()
        return redirect('booking_success')
    booking = Booking.objects.get(id=payment_id)
    return render(request, 'payment.html', {'booking':booking})



def book(request):
    current_user = request.user
    doctors = Doctor.objects.all()
    if request.method == 'POST':
        arrival_date = request.POST['arrival-date']
        departure_date = request.POST['departure-date']
        service = request.POST['service']
        pet_name = request.POST['pet-name']
        pet_type = request.POST['pet-type']
        breed = request.POST['breed']
        problem = request.POST['problem']
        age = request.POST['age']
        weight = request.POST['weight']
        sex = request.POST['sex']
        doctor_id = request.POST['doctor']

        doctor = Doctor.objects.get(id=doctor_id)

        booking = Booking.objects.create(
            user=current_user,
            doctor=doctor,
            arrival_date=arrival_date,
            departure_date=departure_date,
            services=service,
            pet_name=pet_name,
            pet_type=pet_type,
            breed=breed,
            description=problem,
            age=age,
            weight=weight,
            sex=sex
        )
        booking.save()
        
        return redirect(f'payment/{booking.id}')

    return render(request, 'book.html', {'doctors':doctors})

def profile(request):
    user = User.objects.get(id=request.user.id)
    if user.is_superuser == True:
        return redirect('/admin/')
    else:
        customer = Customer.objects.get(user=request.user.id)
        return render(request, 'profile.html', {'page':'profile', 'customer':customer})

def doctor_confirmation(request):
    return render(request, 'doctor_confirmation.html')




def admin_booking_list(request):
    # Check if the user is an admin
    if not request.user.is_staff:
        return redirect('login')  # Redirect non-admins to login page

    # Get search and filter parameters from the request
    query = request.GET.get('query', '')  # Search by customer name
    date_filter = request.GET.get('date', '')  # Filter by arrival date

    # Start with all bookings
    bookings = Booking.objects.all()

    # Filter by customer name (if query provided)
    if query:
        bookings = bookings.filter(user__username__icontains=query)

    # Filter by arrival date (if date_filter provided)
    if date_filter:
        try:
            # Parse the date in the format DD-MM-YYYY
            parsed_date = datetime.strptime(date_filter, "%Y-%m-%d").date()
            # Filter by the date ignoring the time component
            bookings = bookings.filter(arrival_date__date=parsed_date)
        except ValueError:
            # If invalid date format, skip filtering by date
            pass

    # Pass the search and date filter values to the template for consistency
    context = {
        'bookings': bookings,
        'query': query,
        'date_filter': date_filter,
    }
    return render(request, 'admin_booking_list.html', context)








@login_required
def view_customers(request):
    customers = Customer.objects.all()
    return render(request, 'view_customers.html', {'customers': customers})

@login_required
def view_doctors(request):
    doctors = Doctor.objects.all()
    return render(request, 'view_doctors.html', {'doctors': doctors})

# @login_required
# def edit_customer(request, pk):
#     customer = get_object_or_404(Customer, id=pk)

#     if request.method == "POST":
#         customer.user.first_name = request.POST.get('first_name')
#         customer.user.last_name = request.POST.get('last_name')
#         customer.user.email = request.POST.get('email')
#         customer.phone = request.POST.get('phone')
#         customer.address = request.POST.get('address')
#         customer.city = request.POST.get('city')
#         customer.pincode = request.POST.get('pincode')

#         # Handle profile picture
#         if 'remove_pic' in request.POST:  # If remove checkbox is checked
#             if customer.profile_pic:
#                 customer.profile_pic.delete()  # Delete the old profile picture
#                 customer.profile_pic = request.FILES['profile_pic']
        
#         # Handle password change
#         new_password = request.POST.get('new_password')
#         confirm_password = request.POST.get('confirm_password')
#         if new_password and confirm_password:  # If both password fields are filled
#             if new_password == confirm_password:
#                 customer.user.set_password(new_password)  # Update the password
#                 customer.user.save()
#                 messages.success(request, 'Password changed successfully!')
#             else:
#                 messages.error(request, 'Passwords do not match!')
#                 return redirect('edit_customer')  # Redirect back to profile page on error

#         # Save updated details
#         customer.user.save()
#         customer.save()

#         messages.success(request, 'Profile updated successfully!')
#         return redirect('view_customers')


#     return render(request, 'edit_customer.html', {'customer': customer})


# @login_required
# def edit_doctor(request, pk):
#     doctor = get_object_or_404(Doctor, id=pk)
#     if request.method == "POST":
#         doctor.user.first_name = request.POST.get('first_name')
#         doctor.user.last_name = request.POST.get('last_name')
#         doctor.user.email = request.POST.get('email')
#         doctor.phone = request.POST.get('phone')
#         doctor.address = request.POST.get('address')
#         doctor.speacialisation = request.POST.get('speacialisation')
#         doctor.status = request.POST.get('status')

#         # Handle profile picture
#         if 'remove_pic' in request.POST:  # If remove checkbox is checked
#             if doctor.profile_pic:
#                 doctor.profile_pic.delete()  # Delete the old profile picture
#                 doctor.profile_pic = request.FILES['profile_pic']
        
#         # Handle password change
#         new_password = request.POST.get('new_password')
#         confirm_password = request.POST.get('confirm_password')
#         if new_password and confirm_password:  # If both password fields are filled
#             if new_password == confirm_password:
#                 doctor.user.set_password(new_password)  # Update the password
#                 doctor.user.save()
#                 messages.success(request, 'Password changed successfully!')
#             else:
#                 messages.error(request, 'Passwords do not match!')
#                 return redirect('profile')  # Redirect back to profile page on error

#         # Save updated details
#         doctor.user.save()
#         doctor.save()

#         messages.success(request, 'Profile updated successfully!')
#         return redirect('view_doctors')
    
#     return render(request, 'edit_doctor.html', {'doctor': doctor})
