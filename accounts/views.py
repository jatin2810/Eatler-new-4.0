from django.shortcuts import render, HttpResponse, redirect
from django.views.generic import (TemplateView, FormView)
from django.views import View
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
import json
from django.shortcuts import get_object_or_404
from .forms import RegisterForm, LoginForm, PhoneVerificationForm
from .authy_api import send_verfication_code, verify_sent_code
from .models import User
from django.contrib.auth.models import Group
from .decorators import allowed_users

class IndexView(TemplateView):

    template_name = 'accounts/index.html'


class RegisterView(SuccessMessageMixin, FormView):
    template_name = 'accounts/register.html'
    form_class = RegisterForm
    success_message = "One-Time password sent to your registered mobile number.\
                        The verification code is valid for 10 minutes."

    def form_valid(self, form):

        user=self.request.POST

        try:
            response = send_verfication_code(user)
        except Exception as e:
            messages.add_message(self.request, messages.ERROR,
                                'verification code not sent. \n'
                                'Please re-register.')
            return redirect('/register')
        data = json.loads(response.text)

        # print(response.status_code, response.reason)
        # print(response.text)
        # print(data['success'])
        if data['success'] == False:
            messages.add_message(self.request, messages.ERROR,
                            data['message'])
            return redirect('/register')

        else:
            kwargs = {'user': user}
            # print("this is kwargs under register view")
            # print(kwargs)
            self.request.method = 'GET'
            return PhoneVerificationView(self.request,**kwargs)







def view1(request):
    if request.user.is_authenticated:
        return redirect('/')
    # print("under view1 login get request")
    return render(request,'accounts/login.html')

def resend_url(request,phone_number,country_code):

    user={"phone_number":phone_number,"country_code":country_code}
    try:
        response = send_verfication_code(user)
        pass
    except Exception as e:

        # print("Exception while sending verification code")
        messages.add_message(request, messages.ERROR,
                'verification code not sent. \n'
                )
        return redirect('/login')
    data = json.loads(response.text)

    if data['success'] == False:
        messages.add_message(request, messages.ERROR,
        data['message'])
        return redirect('/login')

    # print(response.status_code, response.reason)
    # print(response.text)
    if data['success'] == True:

        request.method = "GET"
        # print(request.method)
        kwargs = {'user':user}
        dict={'user':user}
        return PhoneVerificationView(request,**kwargs)


def LoginView(request):


    # print("under view1 login get request")
    template_name='accounts/login.html'
    # print("Inside login 1")
    if request.method == "POST":
        # print("Inside login post method")
        user=request.POST
        userob = User.objects.filter(phone_number=user['phone_number'])
        if userob:
            try:
                response = send_verfication_code(user)
                pass
            except Exception as e:
                # print("Exception while sending verification code")
                messages.add_message(request, messages.ERROR,
                        'verification code not sent. \n'
                        'Please retry logging in.')
                return redirect('/login')
            data = json.loads(response.text)

            if data['success'] == False:
                    # print("If verifiacation code is not sent by twilio")
                    messages.add_message(request, messages.ERROR,
                    data['message'])
                    return redirect('/login')

            # print(response.status_code, response.reason)
            # print(response.text)
            if data['success'] == True:
                # print("if verification code is sent by twilio")
                request.method = "GET"
                # print(request.method)
                kwargs = {'user':user}
                dict={'user':user}
                return PhoneVerificationView(request,**kwargs)
            else:
                messages.add_message(request, messages.ERROR,
                data['message'])
                return redirect('/login')
        else:
            messages.add_message(request, messages.ERROR,
                    'User does not exist. \n'
                    'Please register.')
            return redirect('/register')

    else:
        return HttpResponse("Not Allowed")












flag=False
user_for_phone_confirmation={}
def PhoneVerificationView(request, **kwargs):
    template_name = 'accounts/phone_confirm.html'
    global flag,user_for_phone_confirmation
    if flag==False and user_for_phone_confirmation=={} and kwargs!={}:
        # print(kwargs['user'])
        user_for_phone_confirmation=kwargs['user']
        flag=True




    if request.method == "POST":
        flag=False
        phone_number = request.POST['phone_number']
        form = PhoneVerificationForm(request.POST)
        if form.is_valid():
            user=user_for_phone_confirmation
            verification_code = request.POST['one_time_password']
            response = verify_sent_code(verification_code, user)
            # print(response.text)
            data = json.loads(response.text)

            if data['success'] == True:
                # flag=False
                try:
                    already=User.objects.get(phone_number=phone_number)
                except:
                    already=None
                if already:
                    login(request, already)
                    if already.groups.filter(name='restaurant').exists():
                        return redirect('/restaurant')

                    return redirect('/index')


                else:
                    userob=User.objects.create(full_name=user['full_name'],
                                            phone_number=user['phone_number'],
                                            country_code=user['country_code'])
                    group = Group.objects.get(name='customer')
                    userob.groups.add(group)
                    # print(userob)
                    login(request, userob)
                    return redirect('/index')
            else:
                messages.add_message(request, messages.ERROR,
                                data['message'])
                user_for_phone_confirmation=user
                return render(request, template_name, {'user':user})
        else:
            context = {
                'user': user,
                'form': form,
            }
            return render(request, template_name, context)

    elif request.method == "GET":
        try:
            user = kwargs['user']
            return render(request, template_name, {'user': user})
        except Exception as e:
            # print("This is Exception")
            # print(e)
            return HttpResponse("Not Allowed")


@login_required
def user_logout(request):
    logout(request)
    global user_for_phone_confirmation
    user_for_phone_confirmation={}
    return redirect('/')





@method_decorator(login_required(login_url="/login/"), name='dispatch')
class DashboardView(SuccessMessageMixin, View):
    template_name = 'accounts/dashboard.html'

    def get(self, request):
        context = {
            'user':self.request.user,
            }
        return render(self.request, self.template_name, {})


@login_required
@allowed_users(allowed_roles=['restaurant'])
def RestaurantView(request):
    template_name="accounts/restaurant.html"
    return render(request,template_name)




# @method_decorator(login_required(login_url="/login/"),name='dispatch')
# @method_decorator(allowed_users(allowed_roles=['restaurant']),name='dispatch')
# class RestaurantView(LoginRequiredMixin,View):
#     template_name="accounts/restaurant.html"
#
#     def get(self,request):
#
#         # restaurant_owner=User.objects.filter(request.user)
#         return render(self.request,self.template_name)   #{'user':restaurant_owner}
