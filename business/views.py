from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from django.utils.decorators import method_decorator
from django.http import HttpResponse, JsonResponse
from django.core.files.storage import FileSystemStorage
from .models import *

import json

# Create your views here.
class IndexView(View):

    template_name = 'index.html'

    def get(self, request):
        return redirect('login')


class SignupView(View):
    template_name = 'signup.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return render(request, self.template_name)

    def post(self, request):
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        try:
            # create an user and mark it as active
            user = User.objects.create_user(first_name = first_name,
                                        last_name = last_name,
                                        username = email,
                                        email = email,
                                        is_active = True)
            user.set_password(password)
            user.save()
        except Exception as e:
            #messages.error(request, 'Try again, email already used in another account.')
            print(e)
            return redirect('signup')
        else:
            #messages.warning(request, 'You have successfully signed up, please login to continue.')
            return redirect('login')


class LoginView(View):

    template_name = 'login.html'

    def get(self, request):
        # if user is already authenticated take them to dashboard
        if request.user.is_authenticated:
            return redirect('dashboard')
        return render(request, self.template_name)

    def post(self, request):
        # if they do not pass email id, give error
        if 'email' not in request.POST:
            return JsonResponse({'error': 'must pass email'}, status=400)
        # if they do not pass password, give error
        if 'password' not in request.POST:
            return JsonResponse({'error': 'must pass password'}, status=400)
        # get the username and password from request
        email = request.POST['email']
        password = request.POST['password']
        # authenticate user
        user = authenticate(request, username=email, password=password)
        if user is not None:
            # log the user in
            login(request, user)
            # redirect user to dashboard
            return redirect('dashboard')
        else:
            return redirect('signin')


class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect('index')


class DashboardView(View):

    template_name = 'dashboard.html'

    @method_decorator(login_required)
    def get(self, request):
        return render(request, self.template_name)


class SearchView(View):

    @method_decorator(login_required)
    def get(self, request):
        # default values of the search
        query = ''
        locality = ''
        limit, offset = (10, 0)

        # get query params from request body
        if 'query' in request.GET:
            query = request.GET['query']

        if 'locality' in request.GET:
            locality = request.GET['locality']

        if 'limit' in request.GET and request.GET['limit'].isnumeric():
            limit = int(request.GET['limit'])

        if 'offset' in request.GET and request.GET['offset'].isnumeric():
            offset = int(request.GET['offset'])

        print('=>', request.GET)

        businesses = [model_to_dict(business) for business in
            UsaRealEstate.objects.filter(name__contains = query, locality__contains = locality)[offset:offset+limit]
        ]

        return JsonResponse({"success": True, "data": businesses}, status=200)


class LocalityView(View):

    @method_decorator(login_required)
    def get(self, request):
        # default values of the search
        query = ''
        limit, offset = (10, 0)

        # get query params from request body
        if 'query' in request.GET:
            query = request.GET['query']

        if 'limit' in request.GET and request.GET['limit'].isnumeric():
            limit = int(request.GET['limit'])

        if 'offset' in request.GET and request.GET['offset'].isnumeric():
            offset = int(request.GET['offset'])

        localities = [self._serialize_cities(city) for city in
            UsaCity.objects.filter(name__contains = query)[offset:offset+limit]
        ]

        return JsonResponse({"success": True, "data": localities})


    def _serialize_cities(self, city):
        city_dict = model_to_dict(city)
        city_dict['locality'] = city.locality
        return city_dict
