from django.contrib import admin
from api.models import Role, Permission, RolePermission, User, EmailValidationStatus
# Register your models here.

admin.site.register(Role)
admin.site.register(Permission)
admin.site.register(RolePermission)
admin.site.register(User)
admin.site.register(EmailValidationStatus)