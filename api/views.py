from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Student, Teacher
from .serializers import StudentSerializer, TeacherSerializer  # Ensure you have a TeacherSerializer, LoginSerializer
import random
import string

def generate_random_password(length=8):
    """Generate a random password."""
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))
# Student Views
@api_view(["POST"])
def create_student(request):
    """Create a new student and return success message."""
    if request.method == "POST":
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            # Generate a new random password
            random_password = generate_random_password()
            serializer.validated_data['password'] = random_password
            
            # Save the student instance
            student = serializer.save()

            return Response(
                {
                    "message": "Student information saved successfully!",
                    "generated_password": random_password,  # Return this for future login
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    serializer = StudentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Student information saved successfully!"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
def get_students(request):
    """Retrieve all student records."""
    if request.method == "GET":
        students = Student.objects.all()  # Retrieve all student records
        serializer = StudentSerializer(students, many=True)  # Serialize the queryset
        return Response(serializer.data, status=status.HTTP_200_OK)  # Return serialized data


@api_view(["POST"])
def login_student(request):
    """Authenticate student and return student data if credentials match."""
    if request.method == "POST":
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            try:
                student = Student.objects.get(email=email)  # Get the Student instance
                if student.check_password(password):  # Check password
                    student_data = {
                        "name": student.name,
                        "email": student.email,
                        "standard": student.standard,
                        "contact_number": student.contact_number,
                        "parent_email": student.parent_email,
                    }
                    return Response(
                        {"message": "Login successful!", "student_data": student_data},
                        status=status.HTTP_200_OK
                    )
                else:
                    return Response(
                        {"message": "Invalid password."},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            except Student.DoesNotExist:
                return Response(
                    {"message": "User not found."},
                    status=status.HTTP_404_NOT_FOUND
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    students = Student.objects.all()
    serializer = StudentSerializer(students, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# Teacher Views

@api_view(["POST"])
def create_teacher(request):
    serializer = TeacherSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Teacher information saved successfully!"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
def get_teachers(request):
    teachers = Teacher.objects.all()
    serializer = TeacherSerializer(teachers, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["GET"])
def get_teacher(request, name):
    try:
        teacher = Teacher.objects.get(name=name)  # Adjust based on your primary key
        serializer = TeacherSerializer(teacher)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Teacher.DoesNotExist:
        return Response({"error": "Teacher not found."}, status=status.HTTP_404_NOT_FOUND)
