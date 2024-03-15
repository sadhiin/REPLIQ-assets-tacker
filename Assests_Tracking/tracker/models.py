import uuid
from django.db import models
from django.contrib.auth.models import User


class Company(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True,primary_key=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    location = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name


class Employee(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    employeid = models.CharField(max_length=255, unique=True)  # Unique employee ID
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    department = models.CharField(max_length=255, blank=True)
    position = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.name} ({self.employeid})"


class Device(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    device_type = models.CharField(max_length=50)  # Phone, Tablet, Laptop, etc.
    device_model = models.CharField(max_length=255)
    serial_number = models.CharField(max_length=255, unique=True)
    condition_on_checkout = models.TextField(blank=True)
    assigned_to = models.ForeignKey(Employee, on_delete=models.SET_NULL, blank=True, null=True)  # Currently assigned employee

    def __str__(self):
        return f"{self.device_type} {self.device_model} ({self.serial_number})"


class CheckoutLog(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    checked_out_at = models.DateTimeField(auto_now_add=True)
    checked_in_at = models.DateTimeField(blank=True, null=True)
    condition_on_return = models.TextField(blank=True)

    def __str__(self):
        return f"Device: {self.device} | Employee: {self.employee} | Checked Out: {self.checked_out_at}"