from api.models import User, RolePermission

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from api.serializers.user_serializers import UserResponseSerializer
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@api_view(['GET'])
def get_users(request):
    # permissions = request.GET.get('permission')
    # if not permissions:
    #     return Response(
    #         {
    #             'message': 'Insufficient access'
    #         },
    #         status=status.HTTP_404_NOT_FOUND
    #     )
    # for p in permission:
    #     decode_permission = hashlib.md5(p.permission.permission_name.decode()).hexdigest()
        
    page_number = request.GET.get('page', 1)
    page_size = request.GET.get('page_size', 10)

    users = User.objects.select_related('role').all()

    paginator = Paginator(users, page_size)
    try:
        users_page = paginator.page(page_number)
        print(users_page.object_list.values())
        serialized_users = UserResponseSerializer(
            users_page.object_list.values(), many=True).data
        return Response(
            {
                "message": "Get user successfully",
                "data": serialized_users,
                "total_pages": paginator.num_pages,
                "current_page": users_page.number,
            },
            status=status.HTTP_200_OK
        )
    except PageNotAnInteger:
        return Response(
            {
                "message": "Invalid page number",
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    except EmptyPage:
        return Response(
            {
                "message": "Page out of range",
            },
            status=status.HTTP_400_BAD_REQUEST
        )

@api_view(['GET'])
def get_user_by_id(request):
    user_id = request.GET.get('user_id')
    if not user_id:
        return Response(
            {
                "message": "User id is required"
            },
            status=status.HTTP_400_BAD_REQUEST
        )
        
    user = User.objects.filter(id=user_id).first()
    if not user:
        return Response(
            {
                "message": "User not found"
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    user_permission = user.get_user_permission()
    return Response(
        {
            "message": "Get user successfully",
            "data": {
                "id": user.id,
                "full_name": user.full_name,
                "email": user.email,
                "account_status": user.account_status,
                "image_url": user.image_url,
                "user_points": user.user_points,
                "permission": user_permission,
                "role": user.role.role_description
            }
        },
        status=status.HTTP_200_OK
    )

@api_view(['PUT'])
def update_user_account_status(request):
    user_id = request.data.get('user_id')
    account_status = request.data.get('account_status')
    if not user_id:
        return Response(
            {
                "message": "User id is required"
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    if not account_status:
        return Response(
            {
                "message": "Account status is required"
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    user = User.objects.filter(id=user_id).first()
    if not user:
        return Response(
            {
                "message": "User not found"
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    user.account_status = account_status
    user.save()
    return Response(
        {
            "message": "Update user successfully",
        },
        status=status.HTTP_200_OK
    )

@api_view(["GET"])
def check_user(request):
    user_id = request.GET.get("user_id")
    if not user_id:
        return Response(
            {
                "message": "User id is required"
            },
            status=status.HTTP_400_BAD_REQUEST
        )
        
    user = User.objects.filter(id=user_id).first()
    if not user:
        return Response(
            {
                "message": False
            },
            status=status.HTTP_200_OK
        )
    return Response(
            {
                "message": True
            },
            status=status.HTTP_200_OK
        )

@api_view(["GET"])
def get_user_by_id_for_ranking_table(request):
    user_id = request.GET.get("user_id")
    if not user_id:
        return Response(
            {
                "message": "User id is required"
            },
            status=status.HTTP_400_BAD_REQUEST
        )
        
    user = User.objects.filter(id=user_id).values("image_url", "full_name").first()
    if not user:
        return Response(
            {
                "message": "User not found"
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    return Response(
        {
            "message": "Get user successfully",
            "data": user
        },
        status=status.HTTP_200_OK
    )


