from django.conf.urls import url
from .views import homepage
from django.urls import path
# from .views import ProductFormView,RestaurantFormView
from .views import (RestaurantCreateView,RestaurantListView,RestaurantDetailView,RestaurantUpdateView,
                    RestaurantDeleteView,ProductCreateView,ProductUpdateView,ProductDeleteView)
app_name='main'

urlpatterns = [
    path('',homepage,name='homepage'),
    # path('add_product/',ProductFormView,name="add_product"),
    # path('add_restaurant/',RestaurantFormView,name="add_restaurant"),
    path('list/',RestaurantListView.as_view(),name="list_restaurant"),
    path('create/',RestaurantCreateView.as_view(),name="create_restaurant"),
    path('list/<int:pk>',RestaurantDetailView.as_view(),name="detail_restaurant"),
    path("update/<int:pk>/",RestaurantUpdateView.as_view(),name="update_restaurant"),
    path("delete/<int:pk>/",RestaurantDeleteView.as_view(),name="delete_restaurant"),

    path('<int:pk>/create_product/',ProductCreateView.as_view(),name="create_product"),
    path('update_product/<int:pk>',ProductUpdateView.as_view(),name="update_product"),
    path('delete_product/<int:pk>',ProductDeleteView.as_view(),name="delete_product"),
]
