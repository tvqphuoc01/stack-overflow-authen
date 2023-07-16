from api.models import User

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def delete_user(request):
    """
    delete user by id or delete a list of users by ids
    """
    
    user_ids = request.data.get('user_ids')
    requester_id = request.data.get('requester_id')
    
    admin = User.objects.filter(id=requester_id).first()
    if admin.role.role_description != 'ADMIN':
        return Response(
            {
                'message': 'Permission denied'
            },
            status=status.HTTP_403_FORBIDDEN
        )
    
    if not user_ids:
        return Response(
            {
                'message': 'Invalid request'
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if len(user_ids) == 1:
        try:
            user = User.objects.filter(id=user_ids[0]).first()
            user.delete()
        except Exception as e:
            return Response(
                {
                    "message": f"Delete user failed {user_ids[0]}",
                    "error": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    else:
        for user_id in user_ids:
            try:
                user = User.objects.filter(id=user_id).first()
                user.delete()
            except Exception as e:
                return Response(
                    {
                        "message": f"Delete user failed {user_id}",
                        "error": str(e)
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
    return Response(
        {
            "message": "Delete user success, number of users deleted: " + str(len(user_ids))
        },
        status=status.HTTP_200_OK
    )
        
        
        
    