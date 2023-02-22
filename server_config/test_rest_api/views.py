from django.http.response import HttpResponse
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate,login as run_login, logout as run_logout
from .functions import save_user,save_user_storage


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
def submitLogin(request):
    data = request.data 
    username = data.get('user_id')
    password = data.get('user_password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        print("success to login")
        run_login(request,user)
        return HttpResponse(status=200)
    else:
        print("fail to login")
    return HttpResponse(status=401) 
    
@api_view(['POST'])
def register(request):
    data = request.data
    username = data.get('user_id')
    save_user(data)
    is_done = save_user_storage(username)
    print(is_done)
    return HttpResponse(is_done,status=200)


@api_view(['POST'])
def logout(request):
    run_logout(request)
    return Response("")
