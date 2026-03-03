from django.db import models
import datetime
from django.contrib.auth.models import User
#this makes the user model created  create a profile for the user
from django.db.models.signals import post_save
# Create your models here.



# create customer profile module
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_modified = models.DateTimeField(User , auto_now=True)
    # first_name = models.CharField(max_length=50)
    # last_name = models.CharField(max_length=50)
    phone= models.CharField(max_length=10, blank=True)
    address1 = models.CharField(max_length=30, blank=True)
    address2 = models.CharField(max_length=30, blank=True)
    city = models.CharField(max_length=20, blank=True)
    state = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=20, blank=True)
    zipcode = models.CharField(max_length=20, blank=True)
    oldcart = models.CharField(max_length=200, blank=True)

    
    
    def __str__(self):
        return  f'{self.user.username}'
    
    #create a user Profile by default when user signs up
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
# Automate the profile thing
post_save.connect(create_profile, sender=User)



#  categories of Products
class Category(models.Model):
    name= models.CharField(max_length=50)

    def __str__(self):
        return self.name
  
class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone= models.CharField(max_length=10)
    email=models.EmailField(max_length=10)
    password=models.CharField(max_length=20)
    
    def __str__(self):
        return  f'{self.first_name} {self.first_name}'

class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(default=0,decimal_places=2,max_digits=6)
    Category=models.ForeignKey(Category, on_delete=models.CASCADE,default=1)
    description= models.CharField(max_length=250,default='',blank=True, null=True)
    image= models.ImageField(upload_to='uploads/product/')

    #add Sale stuff

    is_sale= models.BooleanField(default=False)
    saleprice = models.DecimalField(default=0,decimal_places=2,max_digits=6)

    def __str__(self):
        return self.name
    
class Order(models.Model):
    product= models.ForeignKey(Product, on_delete=models.CASCADE)
    customers= models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)
    address= models.CharField(max_length=100,default='',blank=True, null=True)
    phone= models.CharField(max_length=15,default='',blank=True)
    date= models.DateField(default=datetime.datetime.today)
    status= models.BooleanField(default=False)
   

    def __str__(self):
        return self.product