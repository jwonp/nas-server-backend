import datetime
from io import StringIO
import os
import requests
import json
import zipfile
from urllib import parse

from collections import OrderedDict
from oauth2_provider.views.generic import ProtectedResourceView
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from django.http import FileResponse
from django.core.files.storage import FileSystemStorage
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from .models import UserStorage
from .serializers import StorageSizesSerializer
from django.conf import settings
from .functions import check_file_name_is_valid, convert_path, save_folder_in_files_table, save_folder_in_folders_table,delete_file, add_used_storage_size, delete_file_path
from users.functions import check_remaining_storage_space,save_file,subject_used_storage_size,save_file_path
from .serializers import FileListSerializer
from .models import File
from oauth2_provider.views.base import TokenView
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from oauth2_provider.models import get_access_token_model, get_application_model
from oauth2_provider.signals import app_authorized
class CustomTokenView(TokenView):
    @method_decorator(sensitive_post_parameters("password"))
    def post(self, request, *args, **kwargs):
        url, headers, body, status = self.create_token_response(request)
        if status == 200:
            access_token = json.loads(body).get("access_token")
            if access_token is not None:
                token = get_access_token_model().objects.get(token=access_token)
                app_authorized.send(sender=self, request=request, token=token)
        response = HttpResponse(content=body, status=status)

        for k, v in headers.items():
            response[k] = v
        return response

class ApiEndpoint(ProtectedResourceView):
    def get(self, request, *args, **kwargs):
        return HttpResponse('Hello, OAuth2!')

class Closedpoint(ProtectedResourceView):
    permission_classes = [TokenHasReadWriteScope]
    def get(self, request, *args, **kwargs):
        # print(request.user)
        return HttpResponse('hi there')

class Validtoken(ProtectedResourceView):
    permission_classes = [TokenHasReadWriteScope]
    def get(self, request, *args, **kwargs):
        return JsonResponse({'name':f'{request.user.username}'})

class Refreshtoken(ProtectedResourceView):
    permission_classes = [TokenHasReadWriteScope]
    def post(self, request, *args, **kwargs):

        body = json.loads(request.body)
        refresh_token = body.get('refresh_token')
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
        'refresh_token':refresh_token
        }
        return JsonResponse(result, status=200)

class upload_files(ProtectedResourceView):
    permission_classes = [TokenHasReadWriteScope]
    def post(self, request, *args, **kwargs):
        upload_files = request.FILES.getlist("files")
        username = request.user.username
        # save_path = parse.unquote(request.META.get('HTTP_FILE_PATH'))
        save_path = request.GET.get('File-Path')

        meta_data = []
        files = check_file_name_is_valid(upload_files)
        result_remaining_size = check_remaining_storage_space(upload_files=files, username=username)
        # return JsonResponse({"username":username,'GET':request.GET,'POST':request.POST,"local_path":f'{settings.MEDIA_ROOT}'})
        if(result_remaining_size.get('total_file_size') != -1):
            meta_data = save_file(upload_files=files,username=username,save_path=save_path)
        else:
            return HttpResponse(status=400)
        
        remaining_size = result_remaining_size.get('used_storage_size') - result_remaining_size.get('total_file_size')
        subject_used_storage_size(username=username,remaining_size=remaining_size)
        save_file_path(meta_data=meta_data,username=username)
        return HttpResponse(meta_data,status=200)

            
class delete_files(ProtectedResourceView):
    def post(self,request,*args,**kwargs):
        body = json.loads(request.body)
        file_list = body.get('file_list')
        path =parse.unquote( body.get('path'))
        print('path is ', path)
        username = request.user.username
        
        meta_data = delete_file(delete_files =file_list,username = username,saved_path = path)
        add_used_storage_size(username= username,meta_data=meta_data )
        delete_file_path(username= username, meta_data=meta_data )
        return HttpResponse("")

class get_storage_size(ProtectedResourceView):
    def get(self, request, *args, **kwargs):
        # print(f'getStorageSize,{self.request.user.username}')
        username = self.request.user.username
        print(username)
        storage_sizes = UserStorage.objects.get(username=username)
        serializer = StorageSizesSerializer(storage_sizes, many=False)
        return JsonResponse(data=serializer.data)
        

class add_folder(ProtectedResourceView):
    def post(self, request, *args, **kwargs):
        body = json.loads(request.body)
        path= parse.unquote(body.get('path'))
        converted_path = convert_path(path) +'/'
        username = self.request.user.username
        name = "folder:"+parse.unquote(body.get('folder_name'))

        is_ok_files = save_folder_in_files_table(username=username,name=name,path=converted_path)
        is_ok_folders = save_folder_in_folders_table(username=username,name=name,path=converted_path)
        print(f'{is_ok_files} and {is_ok_folders}')
        return HttpResponse("")

class download_files(ProtectedResourceView):
    def post(self, request, *args, **kwargs):
        body = json.loads(request.body)
        path =convert_path(parse.unquote(body.get('path')))
        username = self.request.user.username
        file_list = body.get('file_list')
        sub_path = f'{username}/{path}'
        # print("file list is ")
        # print(file_list)
        # print("sub path is ")
        # print(sub_path)
        os.chdir(f'{settings.MEDIA_ROOT}/{sub_path}/')
        fs = FileSystemStorage(location=f'{settings.MEDIA_ROOT}/temp')
        with zipfile.ZipFile(f'{settings.MEDIA_ROOT}/temp/{username}.zip', 'w') as file_list_zip:
            for file in file_list:
                file_list_zip.write(f'{file}')
            file_list_zip.close()
        
        response = FileResponse(fs.open(f'{username}.zip','rb'), as_attachment=True)
        return response
            

    
@login_required()
@api_view(['GET'])
def get_file_list_by_path(request,path):
    file_path = path
    file_path = file_path.replace("&","/")
    if(file_path == '내_드라이브'):
        file_path = "/"
    else:
        file_path = file_path + '/'
    file_list = File.objects.filter(file_path=file_path)
    serializer = FileListSerializer(file_list, many=True)
    return Response(serializer.data)
     
    
@login_required()
def secret_page(request, *args, **kwargs):
    return HttpResponse('Secret contents!', status=200)

