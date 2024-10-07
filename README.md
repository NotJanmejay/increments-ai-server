# Steps to create a REST API in Django

`pip install django & pip install djangorestframework`

1. Create a model in api/models.py
2. Create a serializer in api/serializers.py
3. Run migration using `python manage.py makemigrations & python manage.py migrate`
4. Create a view in api/views.py describing the behaviour of your endpoints
5. Add the enpoint url in api/urls.py

---
