from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Student
from .serializers import StudentSerializer


@api_view(["POST"])
def create_student(request):
    if request.method == "POST":
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Student information saved successfully!"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def get_students(request):
    if request.method == "GET":
        students = Student.objects.all()  # Retrieve all student records
        serializer = StudentSerializer(students, many=True)  # Serialize the queryset
        return Response(
            serializer.data, status=status.HTTP_200_OK
        )  # Return serialized data
