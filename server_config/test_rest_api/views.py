import json
import requests
from django.conf import settings
# from django.shortcuts import render

# Create your views here.
# from django.shortcuts import render
# from django.http import JsonResponse
from oauth2_provider.views.base import AuthorizationView
from django.http.response import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate,login as run_login, logout as run_logout
from users.models import User
from django.core.files.storage import FileSystemStorage
# from django.utils.encoding import uri_to_iri
# from .models import Board
# from .serializers import BoardSerializer
# Create your views here.


# def viewjson(request):
#     return JsonResponse("REST API end point...", safe=False)

@api_view(['GET'])
def getStorageSize(request):
    storage_size = {
        'max':100,
        'used':30
    }
    return Response(storage_size)

@api_view(['GET'])
def getFolders(request):
    print("getFolders")
    folders = ["영화","애니","드라마"]
    return Response(folders)



@api_view(['GET'])
def getUser(request):
    print(request.user.username)
    return Response("res")


def submitLogin(request):
    if(request.method == 'POST'):
        data = json.loads(request.body)
        
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
    return HttpResponse(status=404)
    
@api_view(['POST'])
def register(request):
    data = request.data
    user = User.objects.create_user(data.get('user_id'),data.get('user_email'),data.get('user_password'))
    user.last_name = data.get('user_last_name')
    user.first_name = data.get('user_first_name')
    user.save()
    return HttpResponse(status=200)
@api_view(['POST'])
def login(request):
    code = request.data['code']
    print(f"code:{code}")
    url ='http://127.0.0.1:8000/users/o/token/'
    data={
            "client_id":settings.AUTH_DATA['CLIENT_ID'],
            "client_secret":settings.AUTH_DATA['CLIENT_SECRET'],
            "code":code,
            "code_verifier":settings.AUTH_DATA['CODE_VERIFIER'],
            "redirect_uri":"http://127.0.0.1:3000/",
            "grant_type":"authorization_code" 
        }
    headers={'Content-type':'application/x-www-form-urlencoded',"Cache-Control": "no-cache"}
    
    response = requests.post(url,data=data,headers=headers)
    print(response.json())
    access_token = response.json().get('access_token')
    refresh_token = response.json().get('refresh_token')
    result = {
        'access_token':access_token,
        'refresh_token':refresh_token
    }
    # print(f"response:{res_json}")
    return Response(result)

def logout(request):
    if(request.method == 'POST'):
        run_logout(request)
        data = json.loads(request.body)
        print(data.get('token'))
        
        url ='http://127.0.0.1:8000/users/o/revoke-token/'
        revoke_data={
            'token':data.get('token'),
            'client_id':data.get('client_id')
        }
        headers={'Content-type':'application/x-www-form-urlencoded',"Cache-Control": "no-cache"}
        response = requests.post(url,data=json.dumps(revoke_data),headers=headers)
        # print(response.status_code)
        return HttpResponse("")

@api_view(['GET'])
def authorizationview(request):
    print(AuthorizationView.form_class.type())
    return HttpResponse("")

# @api_view(['GET'])
# def index(request):
#     api_urls={
#         'List' : '/boardlist',
#         'Detail' : '/boardlist/<str:pk>/',
#         'Create' : '/boardinsert',
#         'Update' : '/boardupdate/<str:pk>/',
#         'Delete' : '/boarddelete/<str:pk>'
#     }
#     return Response(api_urls)

# @api_view(['GET'])
# def boardList(request):
#     print("boardlist")
#     boards = Board.objects.all()
#     serializer = BoardSerializer(boards, many=True)
#     return Response(serializer.data)

# @api_view(['GET'])
# def boardView(request,pk):
#     boards = Board.objects.get(id=pk)
#     serializer = BoardSerializer(boards, many=False)
#     return Response(serializer.data)

# @api_view(['POST'])
# def boardInsert(request):
#     serializer = BoardSerializer(data=request.data)
    
#     if serializer.is_valid():
#         print("Valid insert...")
#         serializer.save()
#     else:
#         print("inValid insert...")
   
#     return Response(serializer.data)

# @api_view(['PUT'])
# def boardUpdate(request, pk):
#     board = Board.objects.get(id=pk)
#     serializer = BoardSerializer(instance=board,data=request.data)
    
#     if serializer.is_valid():
#         print("Valid update...")
#         serializer.save()
#     else:
#         print("inValid update...")
   
#     return Response(serializer.data)

# @api_view(['DELETE'])
# def boardDelete(request, pk):
#     board = Board.objects.get(id=pk)
    
#     if board:
#        board.delete()
    
#     return Response("Deleted...")

