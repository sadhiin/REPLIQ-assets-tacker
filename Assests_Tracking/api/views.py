from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from tracker.models import User, Company, Employee, Device, CheckoutLog
from .serializers import UserSerializer, CompanySerializer, EmployeeSerializer, DeviceSerializer, CheckoutLogSerializer

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)
        if not user:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        token, created = Token.objects.get_or_create(user=user)
        serializer = UserSerializer(user)
        return Response(serializer.data)


class CompanyListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # only superuser can view all companies
        if request.user.is_superuser:
            companies = Company.objects.all()
        else:
            # other users can only view companies they are associated with  
            companies = Company.objects.filter(users__in=[request.user])

        serializer = CompanySerializer(companies, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CompanySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CompanyDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Company.objects.get(pk=pk)
        except Company.DoesNotExist:
            return None

    def get(self, request, pk):
        company = self.get_object(pk)
        if not company:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CompanySerializer(company)
        return Response(serializer.data)

    def put(self, request, pk):
        company = self.get_object(pk)
        if not company:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CompanySerializer(company, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserCreateView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class DeviceListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get_company(self, request):
        user = request.user
        if not user.is_authenticated:
            return None
        try:
            return user.company.all()[0]  # Assuming user belongs to a single company (adjust if needed)
        except IndexError:
            return None

    def get(self, request):
        company = self.get_company(request)
        if not company:
            return Response(status=status.HTTP_403_FORBIDDEN)  # User not authorized to view devices
        devices = Device.objects.filter(company=company)
        serializer = DeviceSerializer(devices, many=True)
        return Response(serializer.data)

    def post(self, request):
        company = self.get_company(request)
        if not company:
            return Response(status=status.HTTP_403_FORBIDDEN)  # User not authorized to create devices
        serializer = DeviceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(company=company)  # Associate device with the company
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeviceDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Device.objects.get(pk=pk)
        except Device.DoesNotExist:
            return None

    def get(self, request, pk):
        device = self.get_object(pk)
        if not device:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = DeviceSerializer(device)
        return Response(serializer.data)

    def put(self, request, pk):
        device = self.get_object(pk)
        if not device:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = DeviceSerializer(device, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CheckoutLogListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get_company(self, request):
        user = request.user
        if not user.is_authenticated:
            return None
        try:
            return user.company.all()[0]  # Assuming user belongs to a single company (adjust if needed)
        except IndexError:
            return None

    def get(self, request):
        company = self.get_company(request)
        device = request.query_params.get('device', None)  # Optional device filter
        employee = request.query_params.get('employee', None)  # Optional employee filter
        if company:
            checkouts = CheckoutLog.objects.filter(device__company=company)
        else:
            checkouts = CheckoutLog.objects.none()  # Restrict access if not associated with a company
        if device:
            checkouts = checkouts.filter(device__pk=device)
        if employee:
            checkouts = checkouts.filter(employee__pk=employee)
        serializer = CheckoutLogSerializer(checkouts, many=True)
        return Response(serializer.data)

    def post(self, request):
        company = self.get_company(request)
        if not company:
            return Response(status=status.HTTP_403_FORBIDDEN)  # User not authorized to create checkouts
        serializer = CheckoutLogSerializer(data=request.data)
        if serializer.is_valid():
            device_pk = request.data.get('device')
            employee_pk = request.data.get('employee')
            try:
                device = Device.objects.get(pk=device_pk, company=company)  # Ensure device belongs to company
            except Device.DoesNotExist:
                return Response({'error': 'Invalid device provided'}, status=status.HTTP_400_BAD_REQUEST)
            try:
                employee = Employee.objects.get(pk=employee_pk, company=company)  # Ensure employee belongs to company
            except Employee.DoesNotExist:
                return Response({'error': 'Invalid employee provided'}, status=status.HTTP_400_BAD_REQUEST)
            # Check if device is already assigned to another employee before checkout
            if device.assigned_to and device.assigned_to != employee:
                return Response({'error': 'Device is already assigned to another employee'}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save(device=device, employee=employee)
            device.assigned_to = employee  # Update device assignment on checkout
            device.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmployeeListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get_company_object(self, request):
        user = request.user
        if not user.is_authenticated:
            return None
        try:
            return Company.objects.get(users__in=[user])  # Get company associated with the user
        except Company.DoesNotExist:
            return None

    def get(self, request, company_pk):
        company = self.get_company_object(request)
        if not company:
            return Response(status=status.HTTP_403_FORBIDDEN)  # User not authorized to view employees
        employees = Employee.objects.filter(company=company)
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)

    def post(self,request, company_pk):
        company = self.get_company_object(request)
        if not company:
            return Response(status=status.HTTP_403_FORBIDDEN)  # User not authorized to create employees
        request.data['company'] = company.pk
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
