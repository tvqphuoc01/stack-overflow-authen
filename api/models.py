import uuid
import datetime
import logging
import hashlib
from django.db import models
from django.utils.crypto import get_random_string

# Create your models here.
class Role(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role_description=models.CharField(max_length=100, blank=False, default='')
    
    def __str__(self):
        return self.role_description

class Permission(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    permission_name=models.CharField(max_length=100, blank=False, default='')
    permission_description=models.CharField(max_length=100, blank=False, default='')

    def __str__(self):
        return self.permission_description

class RolePermission(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)

class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=100, blank=False, default='')
    email = models.EmailField(max_length=100, blank=False, default='', unique=True)
    password = models.CharField(max_length=100, blank=False, default='')
    account_status = models.CharField(max_length=100, blank=False, default='0')
    image_url = models.CharField(max_length=100, blank=False, default='https://i.pravatar.cc/200')
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    user_points = models.IntegerField(blank=False, default=0)
    
    def __str__(self):
        return self.full_name
    
    def get_user_permission(self):
        user_permission = []
        role_permission = RolePermission.objects.filter(role=self.role)
        for rp in role_permission:
            user_permission.append(rp.permission.permission_name)
        return user_permission
    
    def gen_new_password(self):
        password = get_random_string(length=10)
        try:
            hashed_password = hashlib.md5(password.encode()).hexdigest()
            logging.info(f'Hashed password: {hashed_password}')
        except Exception as e:
            hashed_password = password
        print(hashed_password)
        self.password = hashed_password
        self.save()
        return password
    
class EmailValidationStatus(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=100, blank=False, default='')
    validation_status = models.BooleanField(default=False)
    validation_code = models.CharField(max_length=100, blank=False, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def check_expired(self):
        return self.created_at + datetime.timedelta(days=1) <= datetime.datetime.now()