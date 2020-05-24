from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from main.models import Product,Restaurant
from phonenumber_field.formfields import PhoneNumberField


# class ProductSerializer(ModelSerializer):
#     name = serializers.CharField()
#      = serializers.IntegerField()
#
#     class Meta:
#         model = User
#         fields = ('phone_number','country_code')


class RestaurantSerializer(ModelSerializer):
    query = serializers.CharField()
    class Meta:
        model = Restaurant
        fields = ['query']


class ProductSerializer(ModelSerializer):
    restaurant = serializers.CharField()
    class Meta:
        model = Product
        fields = ['restaurant']
