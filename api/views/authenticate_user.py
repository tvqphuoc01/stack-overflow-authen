import hashlib
import logging
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from api.models import User, EmailValidationStatus, RolePermission
from api.serializers.user_serializers import UserLoginSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def get_user_validation_code(request):
    """
    get user validation code
    """
    user_email = request.GET.get('user_email')
    
    if not user_email:
        return Response(
            {
                'message': 'Invalid request'
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    try:
        user_validation_code = EmailValidationStatus.objects.filter(email=user_email).first()
    except Exception as e:
        return Response(
            {
                'message': 'User not found'
            },
            status=status.HTTP_404_NOT_FOUND
        )
        
    return Response(
        {
            'message': 'Get user validation code success',
            'validation_code': user_validation_code.validation_code
        },
        status=status.HTTP_200_OK
    )

@api_view(['POST'])
def authenticate_user(request):
    """
    Authenticate user with email and password

    Args:
        email : User email
        password : User password
    """
    
    # check request data is valid
    serializer = UserLoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    validated_data = serializer.validated_data
    
    user_email = validated_data.get('email')
    user_password = validated_data.get('password')
    hashed_password = hashlib.md5(user_password.encode()).hexdigest()
    user = User.objects.filter(email=user_email, password=hashed_password).first()
    
    if not user:
        logging.error(f'User not found: {user_email}')
        return Response(
            {
                'message': 'User not found'
            },
            status=status.HTTP_404_NOT_FOUND
        )
    
    verification_status = EmailValidationStatus.objects.filter(user=user).first()
    
    # check if user is verified or not
    # if not verified, return 401
    if verification_status.validation_status == False:
        logging.error(f'User not verified: {user_email}')
        return Response(
            {
                'message': 'User not verified'
            },
            status=status.HTTP_401_UNAUTHORIZED
        )
    # get user permission
    permission = RolePermission.objects.filter(role=user.role)
    user_permission = []
    for p in permission:
        print(p)
        hash_permission = hashlib.md5(p.permission.permission_name.encode()).hexdigest()
        user_permission.append(hash_permission)
    logging.info(f'User authenticated: {user_email}')
    return Response(
        {
            'message': 'User authenticated',
            'user_data': {
                'id': user.id,
                'user_full_name': user.full_name,
                'user_email': user.email,
                'user_permission': user_permission,
            }
        },
        status=status.HTTP_200_OK
    )

@api_view(['POST'])
def reset_password(request):
    """
    Call get_user_validation_code to get reset key before calling this API
    """
    
    user_email = request.data.get('email')
    user_reset_key = request.data.get('reset_key') # get from EmailValidationStatus.validation_code
    
    if not user_email or not user_reset_key:
        return Response(
            {
                'message': 'Invalid request'
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    validation_key = EmailValidationStatus.objects.filter(user__email=user_email).first()
    if not validation_key:
        return Response(
            {
                'message': 'Invalid request'
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if validation_key.validation_code != user_reset_key:
        return Response(
            {
                'message': 'Invalid request'
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # get user data
    user = User.objects.filter(email=user_email).first()
    
    if not user:
        logging.error(f'User not found: {user_email}')
        return Response(
            {
                'message': 'User not found'
            },
            status=status.HTTP_404_NOT_FOUND
        )
        
    # generate new password
    new_temp_password = User.gen_new_password(user)
    try:
        send_mail(
            "RESET PASSWORD",
            f"Your new password is: {new_temp_password}",
            "udptnhom3@gmail.com",
            [user_email],
            fail_silently=False,
        )
    except Exception as e:
        logging.error(f'Error sending email: {e}')
        return Response(
            {
                'message': 'Error sending email'
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    # reset validation key
    new_validation_key = get_random_string(length=5)
    validation_key.validation_code = new_validation_key
    validation_key.save()
    
    return Response(
        {
            'message': 'reset password success',
        },
        status=status.HTTP_200_OK
    )
    
@api_view(['POST'])
def update_password(request):
    """
    Update user password when they change in profile page
    
    Call get_user_validation_code to get reset key before calling this API
    """
    
    user_id = request.data.get('user_id')
    new_password = request.data.get('new_password')
    user_reset_key = request.data.get('reset_key') # get from EmailValidationStatus.validation_code
    
    if not user_id or not new_password or not user_reset_key:
        return Response(
            {
                'message': 'Invalid request'
            },
            status=status.HTTP_400_BAD_REQUEST
        )
        
    # check validation key
    validation_key = EmailValidationStatus.objects.filter(user__id=user_id).first()
    if not validation_key or validation_key.validation_code != user_reset_key:
        return Response(
            {
                'message': 'Invalid request'
            },
            status=status.HTTP_400_BAD_REQUEST
        )
        
    # check valid password
    if len(new_password) < 10:
        return Response(
            {
                'message': 'Please enter a password that is at least 10 characters long'
            },
            status=status.HTTP_400_BAD_REQUEST
        )
        
    # get user data
    user = User.objects.filter(id=user_id).first()
    
    if not user:
        logging.error(f'User not found: {user_id}')
        return Response(
            {
                'message': 'User not found'
            },
            status=status.HTTP_404_NOT_FOUND
        )
    user.password = new_password
    user.save()
    
    return Response(
        {
            'message': 'update password success',
        },
        status=status.HTTP_200_OK
    )
        
    