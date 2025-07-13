from django.urls import path

from credentials import views

urlpatterns = [
    path('customer_register', views.customer_register, name='customer_register'),
    path('login', views.login, name='login'),
    path('doctor_register', views.doctor_register, name='doctor_register'),
    path('logout', views.logout, name='logout'),
    path('book', views.book, name='book'),
    path('booking_success', views.booking_success, name='booking_success'),
    path('profile', views.profile, name='profile'),
    path('payment/<int:payment_id>', views.payment, name='payment'),
    path('doctor_confirmation', views.doctor_confirmation, name='doctor_confirmation'),
    path('admin/bookings/', views.admin_booking_list, name='admin_booking_list'),
    path('admin/customers/', views.view_customers, name='view_customers'),
    path('admin/doctors/', views.view_doctors, name='view_doctors'),
    # path('admin/customers/edit/<int:pk>/', views.edit_customer, name='edit_customer'),
    # path('admin/doctors/edit/<int:pk>/', views.edit_doctor, name='edit_doctor'),
]
