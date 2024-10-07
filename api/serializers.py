from rest_framework import serializers
<<<<<<< HEAD
from .models import Student
from django.contrib.auth.hashers import make_password
=======
from .models import Student, Teacher
>>>>>>> 8b2c37b17dc473e97ae3afac22b4a4f615156537

class StudentSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)  # Optional for initial saving

    class Meta:
        model = Student
        fields = ["name", "email", "standard", "contact_number", "parent_email", "password"]

<<<<<<< HEAD
class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ["email", "password"]

    def create(self, validated_data):
        # Hash the password before saving it
        validated_data['password'] = make_password(validated_data['password'])
        return super(LoginSerializer, self).create(validated_data)
=======


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ["name", "tagline", "description", "greetings", "prompt"]  # Include the new field
>>>>>>> 8b2c37b17dc473e97ae3afac22b4a4f615156537
