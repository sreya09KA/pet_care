from django.db import models
from django.contrib.auth.models import User
from credentials.models import Customer, Doctor
    
class PetLog(models.Model):
    customer=models.ForeignKey(Customer, on_delete=models.CASCADE,null=True)
    doctor=models.ForeignKey(Doctor,on_delete=models.CASCADE,null=True)
    pet = models.CharField(max_length=250)
    date_joined = models.DateTimeField(auto_now_add=True)
    stat=(('Pending','Pending'), ('Treating','Treating'), ('All Done','All Done'), ('Released','Released'))
    status=models.CharField(max_length=50,choices=stat,default='Released',null=True)

    def __str__(self):
        return str(self.customer)
    
class Booking(models.Model):
    service = (
        ('Boarding', 'Boarding'),
        ('Daycare', 'Daycare'),
        ('Grooming', 'Grooming'),
        ('Nutrition', 'Nutrition'),
        ('Veterinary', 'Veterinary')
    )
    pet_type = (
        ('Dog', 'Dog'),
        ('Cat', 'Cat')
    )
    sex = (
        ('Male', 'Male'),
        ('Female', 'Female')
    )
    user = models.ForeignKey(User, on_delete=models.RESTRICT)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, default=None, null=True)
    arrival_date = models.DateTimeField()
    departure_date = models.DateTimeField()
    services = models.CharField(max_length=50,choices=service)
    pet_name = models.CharField(max_length=40)
    pet_type = models.CharField(max_length=10, choices=pet_type)
    breed = models.CharField(max_length=40)
    age = models.PositiveBigIntegerField(null=False)
    weight = models.PositiveIntegerField(null=False)
    sex = models.CharField(max_length=10, choices=sex)
    description = models.TextField()
    status = models.BooleanField(default=False)
    payment_status = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)
    

class Request(models.Model):
    
    pet_log = models.ForeignKey(PetLog, on_delete=models.CASCADE, null = True, blank = True)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, null = True, blank = True)

    def __str__(self):
        return self.booking.description
