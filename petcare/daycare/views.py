from django.shortcuts import get_object_or_404, redirect, render
from django.core.mail import send_mail
from credentials.forms import CustomerForm, DoctorForm, UserUpdateForm
from credentials.models import Customer, Doctor
from daycare.models import Booking
from petcare import settings
from django.contrib import messages, auth
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import make_password
from django.db.models import Q

# Create your views here.

def send_booking_email(subject, message, recipient_email):
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [recipient_email],
        fail_silently=False,
    )

def index(request):
    return render(request, 'index.html')
def about(request):
    return render(request, 'about.html')
def contact(request):
    return render(request, 'contact.html')
def gallery(request):
    return render(request, 'gallery.html')
def main(request):
    return render(request, 'main.html')
def pricing(request):
    return render(request, 'pricing.html')
def services(request):
    return render(request, 'services.html')
def vet(request):
    doctors = Doctor.objects.all()
    return render(request, 'vet.html', {'doctors':doctors})
def blog(request):
    return render(request, 'blog.html')
def appointment(request):
    current_user = request.user
    pet = Booking.objects.filter(user=current_user)
    context = {
        'pet':pet,
    }
    return render(request, 'appointments.html', context)
def base(request):
    user = None
    if 'user_id' in request.session:
        user = Customer.objects.get(id=request.session['user_id'])
    return render(request, 'base.html', {'user',user})


def doctor_dashboard(request):
    current_user = request.user
    doctor = Doctor.objects.get(user=current_user)
    pets = Booking.objects.filter(services='Veterinary').filter(doctor=doctor)
    if request.method == 'POST':
        pet_id = request.POST.get("id")
        status = request.POST.get("status")
        pet = Booking.objects.get(id=pet_id)
        if status == 'accept':
            pet.status = True
            subject = 'Booking Confirmation'
            message = f"Dear {pet.user.first_name},\n\n Your Booking has been confirmed"
            recipient_email = pet.user.email  # Assuming user email is stored in User model
            send_booking_email(subject, message, recipient_email)
        else:
            pet.status = False
            subject = 'Booking Rejected'
            message = f"Dear {pet.user.first_name},\n\nYour booking has been rejected"
            recipient_email = pet.user.email  # Assuming user email is stored in User model
            send_booking_email(subject, message, recipient_email)
        pet.save()
    return render(request, 'doctor_dashboard_main.html', {'page':'dashboard', 'pets':pets})

def doctor_profile(request):
    user = Doctor.objects.get(user=request.user.id)
    return render(request, 'doctor_profile.html', {'page':'doctor_profile', 'user':user})

def edit_doctor_profile(request):
    doctor = get_object_or_404(Doctor, user=request.user)

    if request.method == "POST":
        doctor.user.first_name = request.POST.get('first_name')
        doctor.user.last_name = request.POST.get('last_name')
        doctor.user.email = request.POST.get('email')
        doctor.phone = request.POST.get('phone')
        doctor.address = request.POST.get('address')
        doctor.speacialisation = request.POST.get('speacialisation')
        # doctor.status = request.POST.get('status')

        # Handle profile picture
        if 'remove_pic' in request.POST:  # If remove checkbox is checked
            if doctor.profile_pic:
                doctor.profile_pic.delete()  # Delete the old profile picture
                doctor.profile_pic = request.FILES['profile_pic']
        
        # Handle password change
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        if new_password and confirm_password:  # If both password fields are filled
            if new_password == confirm_password:
                doctor.user.set_password(new_password)  # Update the password
                doctor.user.save()
                messages.success(request, 'Password changed successfully!')
            else:
                messages.error(request, 'Passwords do not match!')
                return redirect('profile')  # Redirect back to profile page on error

        # Save updated details
        doctor.user.save()
        doctor.save()

        messages.success(request, 'Profile updated successfully!')
        # return redirect('view_doctors')
        return redirect('doctor_profile')
    
    return render(request, 'edit_doctor_profile.html', {'doctor': doctor})

def edit_customer_profile(request):
    customer = get_object_or_404(Customer, user=request.user.id)
    if request.method == "POST":
        customer.user.first_name = request.POST.get('first_name')
        customer.user.last_name = request.POST.get('last_name')
        customer.user.email = request.POST.get('email')
        customer.phone = request.POST.get('phone')
        customer.address = request.POST.get('address')
        customer.city = request.POST.get('city')
        customer.pincode = request.POST.get('pincode')

        # Handle profile picture
        if 'remove_pic' in request.POST:  # If remove checkbox is checked
            if customer.profile_pic:
                customer.profile_pic.delete()  # Delete the old profile picture
                customer.profile_pic = request.FILES['profile_pic']
        
        # Handle password change
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        if new_password and confirm_password:  # If both password fields are filled
            if new_password == confirm_password:
                customer.user.set_password(new_password)  # Update the password
                customer.user.save()
                messages.success(request, 'Password changed successfully!')
            else:
                messages.error(request, 'Passwords do not match!')
                return redirect('edit_customer_profile')  # Redirect back to profile page on error

        # Save updated details
        customer.user.save()
        customer.save()

        messages.success(request, 'Profile updated successfully!')
        return redirect('index')

    return render(request, 'edit_customer_profile.html', {'customer': customer})



# def admin_booking_search(request):
#     query = request.GET.get('query', '')
#     date_filter = request.GET.get('date', '')
#     bookings = Booking.objects.all()

#     if date_filter:
#         bookings = bookings.filter(arrival_date__date=date_filter)
#     elif query:
#         bookings = bookings.filter(
#             Q(user__first_name__icontains=query) | 
#             Q(user__last_name__icontains=query)
#         )
    
#     context = {
#         'bookings': bookings,
#         'query': query,
#         'date_filter': date_filter,
#     }
#     return render(request, 'daycare/admin_booking_search.html', context)
