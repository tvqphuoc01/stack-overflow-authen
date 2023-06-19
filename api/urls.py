from django.urls import path
from api.views.create_user import create_new_user

urlpatterns = [
    path('create-user/', create_new_user, name='create_user'),
]