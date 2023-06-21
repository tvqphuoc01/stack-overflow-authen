import hashlib

from api.models import User, EmailValidationStatus, RolePermission
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
    hashed_password = hashlib.md5(user_password.encode()).hexdigest()
    user = User.objects.filter(email=user_email, password=hashed_password).first()
    verification_status = EmailValidationStatus.objects.filter(user=user).first()
    
    # check if user is verified or not
    # if not verified, return 401
    if verification_status.validation_status == False:
        return Response(
            {
                'message': 'User not verified'
            },
            status=status.HTTP_401_UNAUTHORIZED
        )
    if user:
        # get user permission
        permission = RolePermission.objects.filter(role=user.role)
        user_permission = []
        for p in permission:
            user_permission.append(p.permission.permission_name)
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
    else:
        return Response(
            {
                'message': 'User not found'
            },
            status=status.HTTP_404_NOT_FOUND
        )
    