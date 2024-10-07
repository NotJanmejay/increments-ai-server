from django.urls import path
from .views import create_student, get_students

urlpatterns = [
    path("students/", create_student, name="create_student"),
    path("students/all", get_students, name="get_students"),
]
