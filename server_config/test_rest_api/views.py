from django.http.response import HttpResponse

from rest_framework.response import Response
from rest_framework.decorators import api_view
from users.models import User
from .functions import save_user, save_user_storage


@api_view(['POST'])
def getFolders(request):
    print("getFolders")
    folders = []
    return Response(folders)


@api_view(['GET'])
def getUser(request):
    print(request.user.username)
    return Response(request.user.username)


@api_view(['POST'])
def register(request):
    user_count = len(User.objects.all())
    if user_count > 8:
        return HttpResponse(status=400)

    regist_data = request.data
    username = regist_data.get('user_id')

    is_save_user = save_user(regist_data)
    if (is_save_user):
        HttpResponse(status=401)

    is_save_user_storage = save_user_storage(username)
    if (is_save_user_storage == False):
        HttpResponse(status=401)

    return HttpResponse(status=200)
