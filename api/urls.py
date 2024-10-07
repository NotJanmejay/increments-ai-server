from django.urls import path
from .views import create_student, get_students, create_teacher, get_teachers, login_student

urlpatterns = [
    path("students/create/", create_student, name="create_student"),  # Create a new student
    path("students/all//", get_students, name="get_students"),          # Retrieve all students
    path("students/login/", login_student, name="login_student"),      # Student login
    path("teachers/", create_teacher, name="create_teacher"),
    path("teachers/all/", get_teachers, name="get_teachers"),
]