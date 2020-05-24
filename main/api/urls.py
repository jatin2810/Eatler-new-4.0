from django.urls import path
from main.api import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    # path('hello/', views.HelloView.as_view(), name='hello'),
    path('query/',views.getQuery.as_view(), name="query"),
    path('product/',views.getProduct.as_view(), name="product_list"),
    # path('login/',views.login.as_view(),name="login"),

    # path('validate/', ValidateOTP.as_view(), name="validate"),
]

# phone number ->otp jayega->otp verify->token return (Login)

# phone_number/full name/country_code/ ->otp bhejega->otp verify -> databases me save karna
