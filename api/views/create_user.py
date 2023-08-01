# logging
import logging
import hashlib
from django.core.mail import send_mail
from api.models import User, Role, EmailValidationStatus
from api.serializers.user_serializers import UserSerializer

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def create_new_user(request):
    """
        Create new user
        :params request: 
            - full_name
            - email
            - password
            
        :return:
            201 - User created
            400 - Bad request
            500 - Internal server error
    """
    
    # check request data is valid
    serializer = UserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    validated_data = serializer.validated_data
    
    # user info
    name = validated_data.get('full_name')
    email = validated_data.get('email')
    password = validated_data.get('password')
    image_url = request.data.get('image_url', "")
    method = request.data.get('method', 'credential')
    
    try:
        hashed_password = hashlib.md5(password.encode()).hexdigest()
        logging.info(f'Hashed password: {hashed_password}')
    except Exception as e:
        hashed_password = password
    
    # create new user
    try:
        # check if email already taken or not
        # if not, create new user
        account_status = 0
        if (method == "google"):
            account_status = 1
        user, created = User.objects.get_or_create(full_name=name, email=email, password=hashed_password, role=Role.objects.get(role_description='USER'), image_url=image_url, account_status=account_status)
        if created == False:
            if (method == "credential"):
                logging.info(f'Email already taken: {email}')
                return Response(
                    {
                        'message': 'Email already taken'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            elif (method == "google"):
                return Response(
                    {
                        'message': 'Login by google success',
                        'data':{
                            'id': user.id,
                            'user_full_name': user.full_name,
                            'user_email': user.email,
                        }
                    },
                    status=status.HTTP_201_CREATED
                )
        else:
            logging.info(f'User created: {user.__dict__}')
            if (method == "credential"):
                verification_link = f'http://localhost:8006/api/verify-user/?user_id={user.id}'
                send_mail(
                    "VERIFY EMAIL",
                    f"Please verify your email to complete registration by clicking this link: {verification_link}",
                    "udptnhom3@gmail.com",
                    [email],
                    fail_silently=False,
                )
                new_verification_status = EmailValidationStatus.objects.create(user=user, email=email, validation_status=False, validation_code=user.id)
                new_verification_status.save()
                return Response(
                    {
                        'message': 'User created',
                    },
                    status=status.HTTP_201_CREATED
                )
            elif (method == "google"):
                return Response(
                    {
                        'message': 'User created',
                        'data':{
                            'id': user.id,
                            'user_full_name': user.full_name,
                            'user_email': user.email,
                        }
                    },
                    status=status.HTTP_201_CREATED
                )
    except Exception as e:
        return Response(
            {
                'message': 'Internal server error',
                'error': f'{e}'
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )