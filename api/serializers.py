from rest_framework import serializers
from .models import Student
from django.contrib.auth.hashers import make_password

class StudentSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)  # Optional for initial saving

    class Meta:
        model = Student
        fields = ["name", "email", "standard", "contact_number", "parent_email", "password"]

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ["email", "password"]

    def create(self, validated_data):
        # Hash the password before saving it
        validated_data['password'] = make_password(validated_data['password'])
        return super(LoginSerializer, self).create(validated_data)
