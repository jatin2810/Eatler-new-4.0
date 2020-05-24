from django.db import models
from accounts.models import User
from django.shortcuts import redirect
from django.urls import reverse
import os
# Create your models here.



class Restaurant(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=300)
    description = models.TextField()
    photo = models.ImageField(upload_to='restaurant_images',blank=True)
    address = models.CharField(max_length=300)
    city = models.CharField(max_length=200)
    email = models.EmailField()
    contact_number = models.IntegerField()

    def __str__(self):
        return self.name

        
    def get_absolute_url(self):
        return reverse("main:list")



class Product(models.Model):
    restaurant=models.ForeignKey(Restaurant,on_delete=models.CASCADE,related_name="products",default=None)
    name = models.CharField(max_length=300)
    description = models.TextField()
    photo = models.ImageField(upload_to='product_images',blank=True)
    add_ons = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6,decimal_places=2)

    def __str__(self):
        return self.name


    # def get_absolute_image(self):
    #     return os.path.join('/product_images', self.photo.name)
