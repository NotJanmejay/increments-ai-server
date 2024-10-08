from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import make_password, check_password
import random
import string

def generate_random_password(length=8):
    """Generate a random password."""
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

# Student Model
class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    standard = models.CharField(max_length=10)
    contact_number = models.CharField(max_length=15)
    parent_email = models.EmailField()
    password = models.CharField(max_length=128)  # Store hashed password

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Hash the password before saving it if it is not already hashed
        if self.password and not self.password.startswith('pbkdf2_sha256$'):
            self.password = make_password(self.password)
        super(Student, self).save(*args, **kwargs)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
    


    
# Teacher Persona Model
class Teacher(models.Model):
    name = models.CharField(max_length=100, primary_key=True)  # Name as primary key
    tagline = models.CharField(max_length=200)
    description = models.TextField()
    greetings = models.CharField(max_length=255)
    prompt = models.CharField(max_length=2000)  # Storing JSON data
    subject = models.CharField(max_length=100)  # New field for subject


    def __str__(self):
        return self.name