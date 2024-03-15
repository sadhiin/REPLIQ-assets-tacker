from django.urls import path
from .views import (
    LoginView,
    CompanyListCreateView,
    CompanyDetailView,
    UserCreateView,
    EmployeeListCreateView,
    DeviceListCreateView, DeviceDetailView, CheckoutLogListCreateView)

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('companies/', CompanyListCreateView.as_view(), name='company-list'),
    path('companies/<int:pk>/', CompanyDetailView.as_view(), name='company-detail'),
    path('users/', UserCreateView.as_view(), name='user-create'),
    path('companies/<int:company_pk>/employees/', EmployeeListCreateView.as_view(), name='employee-list'),
    path('devices/', DeviceListCreateView.as_view(), name='device-list'),
    path('devices/<int:pk>/', DeviceDetailView.as_view(), name='device-detail'),
    path('checkouts/', CheckoutLogListCreateView.as_view(), name='checkout-list'),
]
