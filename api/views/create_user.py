from django_cryptography.fields import encrypt

from api.models import User
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
    
    try:
        hashed_password = encrypt(password)
    except Exception as e:
        hashed_password = password
    
    # create new user
    try:
        # check if email already taken or not
        # if not, create new user
        created = User.objects.get_or_create(full_name=name, email=email, password=hashed_password)
        if created:
            return Response(
                {
                    'message': 'Email already taken'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            return Response(
                {
                    'message': 'User created'
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