# forms.py
from django.contrib.auth.forms import UserChangeForm
from django import forms
from .models import Customer, Doctor
from django.contrib.auth.models import User

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['profile_pic', 'phone', 'address', 'pincode', 'city']

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['profile_pic', 'phone', 'address', 'speacialisation', 'status']

class DoctorProfileForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['profile_pic', 'phone', 'address', 'speacialisation', 'status']

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
