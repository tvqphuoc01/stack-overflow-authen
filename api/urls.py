from django.urls import path
from api.views.create_user import create_new_user
from api.views.authenticate_user import authenticate_user
from api.views.email_verifcation import verify_user
from api.views.get_user import get_users, get_user_by_id, update_user_account_status, check_user

urlpatterns = [
    path('create-user', create_new_user, name='create_user'),
    path('authenticate', authenticate_user, name='authenticate'),
    path('verify-user', verify_user, name='verify_user'),
    path('users', get_users, name='user_list'),
    path('get-user-by-id', get_user_by_id, name='get_user_by_id'),
    path('update-user-account-status', update_user_account_status, name='update_user_account_status'),
    path('check-user', check_user, name='check_user')
]
