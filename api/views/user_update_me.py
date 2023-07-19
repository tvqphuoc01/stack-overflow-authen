from api.models import User

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from api.serializers.user_serializers import RequestUserSerializer


@api_view(['PUT'])
def user_update_me(request):
    # check request data is valid
    serializer = RequestUserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    validated_data = serializer.validated_data
    
    user = validated_data.get('user')
    full_name = request.data.get("full_name", user.full_name)
    image_url = request.data.get("image_url", user.image_url)

    if (user.full_name != full_name):
        user.full_name = full_name

    if (user.image_url != image_url):
        user.image_url = image_url

    user.save()

    return Response(
        {
            "message": "Update successfully"
        },
        status=status.HTTP_200_OK
    )

