from django.urls import path
from api.views.create_user import create_new_user
from api.views.authenticate_user import authenticate_user, reset_password, get_user_validation_code, update_password
from api.views.email_verifcation import verify_user
from api.views.get_user import get_users, get_user_by_id, update_user_account_status, check_user, get_user_by_id_for_ranking_table
from api.views.delete_user import delete_user
from api.views.update_user import user_update_me

urlpatterns = [
    path('create-user', create_new_user, name='create_user'),
    path('authenticate', authenticate_user, name='authenticate'),
    path('verify-user', verify_user, name='verify_user'),
    path('users', get_users, name='user_list'),
    path('get-user-by-id', get_user_by_id, name='get_user_by_id'),
    path('update-user-account-status', update_user_account_status, name='update_user_account_status'),
    path('check-user', check_user, name='check_user'),
    path('get-user-by-id-for-ranking-table', get_user_by_id_for_ranking_table, name='get_user_by_id_for_ranking_table'),
    path('get-user-validation-code', get_user_validation_code, name='get_user_validation_code'),
    path('reset-password', reset_password, name='reset_password'),
    path('update-password', update_password, name='update_password'),
    path('delete-user', delete_user, name='delete_user'),
    path('user-update-me', user_update_me, name='user_update_me')
]
