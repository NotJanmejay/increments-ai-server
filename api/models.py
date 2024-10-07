from django.db import models


# Create your models here.
class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    standard = models.CharField(max_length=10)
    contact_number = models.CharField(max_length=15)
    parent_email = models.EmailField()

    def __str__(self):
        return self.name
