from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.FileField(upload_to='profile_pic/CustomerProfilePic/',null=True,blank=True)
    phone = models.CharField(max_length=10, default='0')
    address = models.CharField(max_length=250)
    pincode = models.PositiveBigIntegerField(default=0)
    city = models.CharField(max_length=250, default='Kochi')
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)

    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    
    @property
    def get_id(self):
        return self.user.id
    
    def __str__(self):
        return self.user.first_name
    
class Doctor(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.FileField(upload_to='profile_pic/DoctorProfilePic/',null=True,blank=True)
    phone = models.CharField(max_length=10, default='0')
    address = models.CharField(max_length=250)
    speacialisation = models.CharField(max_length=250)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    status = models.BooleanField(default=False)

    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    
    @property
    def get_id(self):
        return self.user.id
    
    def __str__(self):
        return self.user.first_name
    




      
    