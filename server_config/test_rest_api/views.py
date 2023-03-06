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
        return HttpResponse(user_count, status=200)
    data = request.data
    username = data.get('user_id')
    save_user(data)
    is_done = save_user_storage(username)
    return HttpResponse(is_done, status=200)
