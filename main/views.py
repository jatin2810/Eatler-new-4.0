from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.views.generic import (View,TemplateView,ListView,DetailView,
                                    CreateView,UpdateView,DeleteView)
from .models import Product,Restaurant
from .forms import ProductForm,RestaurantForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from accounts.decorators import allowed_users

def homepage(request):
    return render(request,'main/index.html')


#
# def ProductFormView(request):
#     if request.method=="POST":
#         product_form = ProductForm(data=request.POST)
#         if product_form.is_valid():
#             product=product_form.save()
#             if 'photo' in request.FILES:
#                 product.photo=request.FILES['photo']
#             product.save()
#         else:    #in case if there is error in validation of input data
#             print(product_form.errors)
#         return redirect("/restaurant")
#     else:      #in case if the method is not post
#         product_form=ProductForm()
#
#     context_dic={"product_form":product_form}
#     return render(request,"main/add_product.html",context_dic)
#
#
# def RestaurantFormView(request):
#     if request.method=="POST":
#         restaurant_form = RestaurantForm(data=request.POST)
#         if restaurant_form.is_valid():
#
#             restaurant=restaurant_form.save(commit=False)
#             restaurant.user = request.user
#             if 'photo' in request.FILES:
#                 restaurant.photo=request.FILES['photo']
#             restaurant.save()
#         else:    #in case if there is error in validation of input data
#             print(restaurant_form.errors)
#         return redirect("/restaurant")
#     else:      #in case if the method is not post
#         restaurant_form=RestaurantForm()
#
#     context_dic={"restaurant_form":restaurant_form}
#     return render(request,"main/add_restaurant.html",context_dic)





@method_decorator(login_required(login_url="/login/"), name='dispatch')
@method_decorator(allowed_users(allowed_roles=['restaurant']),name='dispatch')
class RestaurantListView(ListView):
    context_object_name="restaurants"
    def get_queryset(self):
        return Restaurant.objects.filter(user=self.request.user)

@method_decorator(login_required(login_url="/login/"), name='dispatch')
@method_decorator(allowed_users(allowed_roles=['restaurant']),name='dispatch')
class RestaurantCreateView(CreateView):
    fields=('name','description','photo','address','city','email','contact_number')
    model=Restaurant
    def form_valid(self, form):

        form.instance.user = self.request.user
        if 'photo' in self.request.FILES:
            form.instance.photo=self.request.FILES['photo']
        # print(self.request.user)
        return super(RestaurantCreateView, self).form_valid(form)
    success_url=reverse_lazy("main:list_restaurant")


@method_decorator(login_required(login_url="/login/"), name='dispatch')
@method_decorator(allowed_users(allowed_roles=['restaurant']),name='dispatch')
class RestaurantDetailView(DetailView):
    context_object_name="restaurant_details"
    model = Restaurant


@method_decorator(login_required(login_url="/login/"), name='dispatch')
@method_decorator(allowed_users(allowed_roles=['restaurant']),name='dispatch')
class RestaurantUpdateView(UpdateView):
    fields=("name","description","photo","email","contact_number")
    def get_queryset(self):
        return Restaurant.objects.filter(user=self.request.user)

    def get_success_url(self):
          return reverse_lazy('main:detail_restaurant', kwargs={'pk': self.kwargs['pk']})



@method_decorator(login_required(login_url="/login/"), name='dispatch')
@method_decorator(allowed_users(allowed_roles=['restaurant']),name='dispatch')
class RestaurantDeleteView(DeleteView):
    def get_queryset(self):
        return Restaurant.objects.filter(user=self.request.user)
    success_url=reverse_lazy("main:list_restaurant")




#
# @method_decorator(login_required(login_url="/login/"), name='dispatch')
# @method_decorator(allowed_users(allowed_roles=['restaurant']),name='dispatch')
# class RestaurantListView(ListView):
#     context_object_name="restaurants"
#     def get_queryset(self):
#         return Restaurant.objects.filter(user=self.request.user)

@method_decorator(login_required(login_url="/login/"), name='dispatch')
@method_decorator(allowed_users(allowed_roles=['restaurant']),name='dispatch')
class ProductCreateView(CreateView):
    # fields=('name','description','photo','add_ons','price')
    model=Product
    form_class=ProductForm
    def form_valid(self, form):
        product = form.save(commit=False)
        photo = form.cleaned_data['photo']
        restaurantID=self.kwargs['pk']
        restaurant=Restaurant.objects.get(pk=restaurantID)
        form.instance.restaurant = restaurant
        form.instance.photo=photo
        product.save()
        return super(ProductCreateView, self).form_valid(form)
    def get_success_url(self):
          return reverse_lazy('main:detail_restaurant', kwargs={'pk': self.kwargs['pk']})





@method_decorator(login_required(login_url="/login/"), name='dispatch')
@method_decorator(allowed_users(allowed_roles=['restaurant']),name='dispatch')
class ProductUpdateView(UpdateView):
    fields=('name','description','photo','add_ons','price')
    restaurantID = None
    def get_queryset(self):
        global restaurantID
        productID=self.kwargs['pk']
        product=Product.objects.get(pk=productID)
        restaurant=product.restaurant
        restaurantID=restaurant.pk
        return Product.objects.filter(restaurant=restaurant)


    def get_success_url(self):
          return reverse_lazy('main:detail_restaurant',kwargs={'pk': restaurantID})



@method_decorator(login_required(login_url="/login/"), name='dispatch')
@method_decorator(allowed_users(allowed_roles=['restaurant']),name='dispatch')
class ProductDeleteView(DeleteView):
    restaurantID = None
    def get_queryset(self):
        global restaurantID
        productID=self.kwargs['pk']
        product=Product.objects.get(pk=productID)
        restaurant=product.restaurant
        restaurantID=restaurant.pk
        return Product.objects.filter(restaurant=restaurant)


    def get_success_url(self):
          return reverse_lazy('main:detail_restaurant',kwargs={'pk': restaurantID})
