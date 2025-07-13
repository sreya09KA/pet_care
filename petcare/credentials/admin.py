from django.contrib import admin

from credentials.models import Customer, Doctor

# Register your models here.

class DoctorAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'address', 'speacialisation', 'date_joined', 'status']
    list_editable = ['status']


admin.site.register(Customer)
admin.site.register(Doctor, DoctorAdmin)
