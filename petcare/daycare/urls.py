from django.urls import path

from daycare import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('gallery/', views.gallery, name='gallery'),
    path('main/', views.main, name='main'),
    path('blog/', views.blog, name='blog'),
    path('pricing/', views.pricing, name='pricing'),
    path('services/', views.services, name='services'),
    path('vet/', views.vet, name='vet'),
    path('appointment/', views.appointment, name='appointment'),
    
    # path('admin/bookings/search/', views.admin_booking_search, name='admin_booking_search'),
    path('profile/edit/', views.edit_customer_profile, name='edit_customer_profile'),
    path('doctor_dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('doctor_profile/', views.doctor_profile, name='doctor_profile'),
    path('doctor_profile/edit/', views.edit_doctor_profile, name='edit_doctor_profile'),
]