import json
from django.http import JsonResponse
import requests
from django.conf import settings
# from django.shortcuts import render

# Create your views here.
# from django.shortcuts import render
# from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from oauth2_provider.views.base import AuthorizationView
from django.http.response import HttpResponse
from django.views import View
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate,login as run_login, logout as run_logout
from .functions import save_user,save_user_storage
# from django.utils.encoding import uri_to_iri
# from .models import Board
# from .serializers import BoardSerializer
# Create your views here.


# def viewjson(request):
#     return JsonResponse("REST API end point...", safe=False)


@api_view(['POST'])
def getFolders(request):
    print("getFolders")
    folders = []
    return Response(folders)



@api_view(['GET'])
def getUser(request):
    print(request.user.username)
    return Response("res")

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


# @api_view(['POST'])
# def login(request):
class login(View):
    # @method_decorator(csrf_exempt)
    def post(self, request, *args, **kwargs):
        # code = request.data['code']
        isAuthed = request.user.is_authenticated
        code = json.loads(request.body).get('code')
        print(f"code:{code}")
        url ='http://api.ikiningyou.com/users/o/token/'
        data={
                "client_id":settings.AUTH_DATA['CLIENT_ID'],
                "client_secret":settings.AUTH_DATA['CLIENT_SECRET'],
                "code":code,
                "code_verifier":settings.AUTH_DATA['CODE_VERIFIER'],
                "redirect_uri":"http://www.ikiningyou.com/",
                "grant_type":"authorization_code" 
            }
        headers={'Content-type':'application/x-www-form-urlencoded',"Cache-Control": "no-cache"}
        return JsonResponse(data=data)
        token_response = requests.post(url,data=json.dumps(data),headers=headers)
        return JsonResponse({'status':token_response.status_code})
        access_token = token_response.json().get('access_token')
        refresh_token = token_response.json().get('refresh_token')
        result = {
            'access_token':access_token,
        }
        print(result)
        # headers={'Content-type':'application/json'}
        response = JsonResponse(data=result)
        response.set_cookie( key='refresh',value=refresh_token,httponly=True)
        return response
    # return Response(data=result,headers=headers)

@api_view(['POST'])
def logout(request):
    run_logout(request)
    data = request.data
    print(data.get('token'))
    
    url ='http://api.ikiningyou.com/users/o/revoke-token/'
    revoke_data={
        'token':data.get('token'),
        'client_id':settings.AUTH_DATA.get('CLIENT_ID')
    }
    headers={'Content-type':'application/x-www-form-urlencoded',"Cache-Control": "no-cache"}
    requests.post(url,data=json.dumps(revoke_data),headers=headers)
    return Response("")

@api_view(['GET'])
def authorizationview(request):
    print(AuthorizationView.form_class.type())
    return HttpResponse("")

@api_view(['GET'])
def refresh_token(request):
    refresh_token = request.COOKIES['refresh']
    print(f'refresh_token : {refresh_token}')
    url ='http://api.ikiningyou.com/users/o/token/'
    data={
        "grant_type":"refresh_token", 
        "refresh_token":refresh_token,
        "client_id":settings.AUTH_DATA['CLIENT_ID'],
        "client_secret":settings.AUTH_DATA['CLIENT_SECRET']
    }
    headers={'Content-type':'application/x-www-form-urlencoded',"Cache-Control": "no-cache"}
    response = requests.post(url,data=data,headers=headers)
    access_token = response.json().get('access_token')
    refresh_token = response.json().get('refresh_token')

    result = {
    'access_token':access_token,
    }
    print(result)
    response = Response(result)
    response.set_cookie(key='refresh',value=refresh_token,httponly=True)
    return response
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

