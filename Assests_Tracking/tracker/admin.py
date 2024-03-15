from django.contrib import admin
from .models import Company, Device, Employee, CheckoutLog


admin.site.register(Company)
admin.site.register(Device)
admin.site.register(Employee)
admin.site.register(CheckoutLog)