from django.urls import path
from .views import create_student, get_students, login_student

urlpatterns = [
    path("students/create/", create_student, name="create_student"),  # Create a new student
    path("students/all/", get_students, name="get_students"),          # Retrieve all students
    path("students/login/", login_student, name="login_student"),      # Student login
]
