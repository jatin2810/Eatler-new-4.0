from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from main.models import Restaurant,Product
from django.shortcuts import get_object_or_404
from main.api.serializers import (
    RestaurantSerializer,ProductSerializer
)
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
import json

from django.http import JsonResponse
from django.forms.models import model_to_dict




class getQuery(CreateAPIView):
    serializer_class = RestaurantSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(
            data=request.data,
        )
        if serializer.is_valid():
            query = serializer.validated_data['query']
            print(query)
            restaurant_list=Restaurant.objects.raw(query)
            # print(restaurant_list)
            # dict={}
            # for object in restaurant_list:
            #     # dict[object.name] = []  # converts ValuesQuerySet into Python list
            #     # dict[object.name]={'city':object.city,'address':object.address,'photo':object.photo,'description':object.description,'email':object.email,'contact_number':object.contact_number}
            dict1={}
            i=0
            for object in restaurant_list:
                # dict= model_to_dict(object)
                dict1[i]={'name':object.name,'city':object.city,'address':object.address,'description':object.description,'email':object.email,'contact_number':object.contact_number}
                i=i+1
            print(dict1)
            return Response(dict1)




class getProduct(CreateAPIView):
    serializer_class = ProductSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(
            data=request.data,
        )
        if serializer.is_valid():
            restaurant = serializer.validated_data['restaurant']
            print(restaurant)
            restaurantID=Restaurant.objects.filter(name=restaurant).first()
            print(restaurantID)
            product=Product.objects.filter(restaurant=restaurantID)
            dict1={}
            i=0
            for object in product:
                # dict= model_to_dict(object)
                dict1[i]={'name':object.name,'description':object.description,'add_ons':object.add_ons,'price':object.price}
                i=i+1
            print(dict1)
            return Response(dict1)
