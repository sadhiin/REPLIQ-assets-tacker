from django.shortcuts import render, redirect
from django.http import HttpResponse
# Create your views here.

def index(request):
    routes = [
        {'POST': "api/users/token/"}, # for generating json web token
        # {'POST': "api/users/token/refresh/"}, # for getting a new token after a time.
        # {'GET': "api/companies/"},
        # {'GET': "api/companies/id"},
        # {'GET': "api/devices/"},
        # {'GET': "api/devices/id"},
        # {'GET': "api/employees/"},
        # {'GET': "api/employees/id"},
        # {'GET': "api/checkoutlogs/"},
        {'GET': "api/checkoutlogs/id"},
    ]
    return HttpResponse(route for route in routes)  # Serialize the data and return a Response object
