from api.models import User, EmailValidationStatus

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def verify_user(request):
    """
        Verify user by verification Link
        'http://localhost:8006/api/verify-user/?user_id={user_id}'
    """
    # get user id from request
    user_id = request.GET.get('user_id')
    
    # get user by id
    user = User.objects.filter(id=user_id)
    
    if user:
        try:
            EmailValidationStatus.objects.filter(user=user[0]).update(validation_status=True)
            user.account_status = 1
            user.save()
            return Response(
                {
                    'message': 'Verify user successfully',
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {
                    'message': 'Verify user failed',
                    'error': str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    else:
        return Response(
            {
                'message': 'User not found'
            },
            status=status.HTTP_404_NOT_FOUND
        )