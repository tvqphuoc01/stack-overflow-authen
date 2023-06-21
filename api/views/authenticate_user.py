from api.models import User, EmailValidationStatus
from api.serializers.user_serializers import UserLoginSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

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
    
    user = User.objects.filter(email=user_email, password=user_password)
    verification_status = EmailValidationStatus.objects.filter(user=user[0])
    
    # check if user is verified or not
    # if not verified, return 401
    if verification_status[0].validation_status == False:
        return Response(
            {
                'message': 'User not verified'
            },
            status=status.HTTP_401_UNAUTHORIZED
        )
        
    if user:
        return Response(
            {
                'message': 'User authenticated',
                'user_data': {
                    'id': user[0].id,
                    'user_full_name': user[0].full_name,
                    'user_email': user[0].email,
                    
                }
            },
            status=status.HTTP_200_OK
        )
    else:
        return Response(
            {
                'message': 'User not found'
            },
            status=status.HTTP_404_NOT_FOUND
        )
    