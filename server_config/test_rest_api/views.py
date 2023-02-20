import json
from django.http import JsonResponse
import requests
from django.conf import settings

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from oauth2_provider.views.base import AuthorizationView
from django.http.response import HttpResponse
from django.views import View
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


# @api_view(['POST'])
# def login(request):
class login(View):
    # @method_decorator(csrf_exempt)
    def post(self, request, *args, **kwargs):
        # code = request.data['code']

        code = json.loads(request.body).get('code')
        print(f"code:{code}")
        # url ='https://api.ikiningyou.com/getusers/'
        url ='https://api.ikiningyou.com/users/o/token/'
        data={
                "client_id":settings.AUTH_DATA['CLIENT_ID'],
                "client_secret":settings.AUTH_DATA['CLIENT_SECRET'],
                "code":code,
                "code_verifier":settings.AUTH_DATA['CODE_VERIFIER'],
                "redirect_uri":"https://www.ikiningyou.com/",
                "grant_type":"authorization_code" 
            }
        headers={'Content-type':'application/x-www-form-urlencoded',"Cache-Control": "no-cache"}
        token_response = requests.post(url,data=data,headers=headers)
        # token_response = requests.get(url,verify=False)
        # return token_response
        
        # response = requests.get('https://api.ikiningyou.com/getuser/')
        # return HttpResponse(token_response.status_code)
        # return JsonResponse(response.json())
        access_token = token_response.json().get('access_token')
        refresh_token = token_response.json().get('refresh_token')
        result = {
            'access_token':access_token,
        }
        # print(result)
        # response_header={ 
        #     "Access-Control-Allow-Origin":"*",
        #     "Access-Control-Allow-Methods":"GET,HEAD,OPTIONS,POST,PUT",
        #     "Access-Control-Allow-Headers":"Origin, X-Requested-With, Content-Type, Accept, Authorization, Access-Control-Allow-Methods"
        # }
        
        response = JsonResponse(data=result,headers=response_header)
        
        response.set_cookie( key='refresh',value=refresh_token,httponly=True)
        return response
    # return Response(data=result,headers=headers)

@api_view(['POST'])
def logout(request):
    run_logout(request)
    # data = request.data
    # print(data.get('token'))
    
    # url ='https://api.ikiningyou.com/users/o/revoke-token/'
    # revoke_data={
    #     'token':data.get('token'),
    #     'client_id':settings.AUTH_DATA.get('CLIENT_ID')
    # }
    # headers={'Content-type':'application/x-www-form-urlencoded',"Cache-Control": "no-cache"}
    # requests.post(url,data=json.dumps(revoke_data),headers=headers)
    return Response("")



@api_view(['GET'])
def refresh_token(request):
    refresh_token = request.COOKIES['refresh']
    print(f'refresh_token : {refresh_token}')
    url ='https://api.ikiningyou.com/users/o/token/'
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


