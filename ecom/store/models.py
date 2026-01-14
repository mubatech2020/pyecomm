from django.db import models
import datetime
# Create your models here.
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