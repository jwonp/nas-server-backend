import requests
import json
from django.conf import settings
from oauth2_provider.views.generic import ProtectedResourceView
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from .serializers import FileSerializer
from .models import File
class ApiEndpoint(ProtectedResourceView):
    def get(self, request, *args, **kwargs):
        return HttpResponse('Hello, OAuth2!')

class Closedpoint(ProtectedResourceView):
    permission_classes = [TokenHasReadWriteScope]
    def get(self, request, *args, **kwargs):
        print(request.user)
        return HttpResponse('hi there')

class Validtoken(ProtectedResourceView):
    permission_classes = [TokenHasReadWriteScope]
    def get(self, request, *args, **kwargs):
        return JsonResponse({'name':f'{request.user.username}'}, status=200)

class Refreshtoken(ProtectedResourceView):
    permission_classes = [TokenHasReadWriteScope]
    def post(self, request, *args, **kwargs):
        
        body = json.loads(request.body)
        refresh_token = body.get('refresh_token')

        
        url ='http://127.0.0.1:8000/users/o/token/'
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
        print(f"access_token:{access_token}")
        print(f"refresh_token:{refresh_token}")
        result = {
        'access_token':access_token,
        'refresh_token':refresh_token
        }
        return JsonResponse(result, status=200)

class upload_files(ProtectedResourceView):
    permission_classes = [TokenHasReadWriteScope]
    def post(self, request, *args, **kwargs):
        username = request.user.username
        save_path = request.META.get('HTTP_FILE_PATH')
        sub_path = f'{username}/{save_path}'
        print(sub_path)
        # print(username)
        # print("media root "+settings.MEDIA_ROOT)
        upload_files = request.FILES.getlist("files")
        fs = FileSystemStorage(location=f'{settings.MEDIA_ROOT}/{sub_path}/')
        result_meta_data = []
        
        for item in upload_files:
            file_name = fs.save(item.name, item)
            file_path = fs.path(file_name)
            # file_owner = get_user_id()
            result_meta_data.append({file_name:file_path})
        

        return HttpResponse(result_meta_data)

class getFileListByPath(ProtectedResourceView):
    permission_classes = [TokenHasReadWriteScope]
    def get(self, request, *args, **kwargs):
        path = request.GET.get('path')
        file_list = File.objects.get(file_path = path)
        serializer = FileSerializer(file_list, many=True)
        return Response(serializer.data)
    
login_required()
def secret_page(request, *args, **kwargs):
    return HttpResponse('Secret contents!', status=200)

