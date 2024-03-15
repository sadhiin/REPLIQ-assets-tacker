from rest_framework import serializers
from rest_framework.authtoken.models import Token
from tracker.models import User, Company, Employee, Device, CheckoutLog


class UserSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'token')
        extra_kwargs = {'password': {'write_only': True}}

    def get_token(self, obj):
        token, created = Token.objects.get_or_create(user=obj)
        return token.key


class CompanySerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Company
        fields = '__all__'


class EmployeeSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)

    class Meta:
        model = Employee
        fields = '__all__'


class DeviceSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    assigned_to = EmployeeSerializer(read_only=True)

    class Meta:
        model = Device
        fields = '__all__'


class CheckoutLogSerializer(serializers.ModelSerializer):
    device = DeviceSerializer(read_only=True)
    employee = EmployeeSerializer(read_only=True)

    class Meta:
        model = CheckoutLog
        fields = '__all__'
