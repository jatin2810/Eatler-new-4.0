from django import forms
from django.conf import settings
from django.utils.translation import ugettext as _
from django.contrib.auth import authenticate
from .models import Product,Restaurant





class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields=['name','description','photo','add_ons','price']



class RestaurantForm(forms.ModelForm):

    class Meta:
        model = Restaurant
        fields=['name','description','photo','address','city','email','contact_number']
