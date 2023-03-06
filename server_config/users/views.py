
import os

import json
import zipfile
from urllib import parse

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
from .functions import check_file_name_is_valid, convert_path, delete_by_selected, delete_temp_file, get_all_by_table_switch, root_path_slash, save_folder_in_files_table, save_folder_in_folders_table, delete_file, add_used_storage_size, delete_file_path
from users.functions import check_remaining_storage_space, save_file, subject_used_storage_size, save_file_path
from .serializers import FileListSerializer
from .models import File


# admin
class check_admin(ProtectedResourceView):
    def get(self, request, *args, **kwargs):
        username = self.request.user.username
        if username != settings.ADMIN_USER:
            return HttpResponse(f'{username},{settings.ADMIN_USER}', status=400)
        return HttpResponse(status=200)


class get_all_data(ProtectedResourceView):
    permission_classes = [TokenHasReadWriteScope]

    def post(self, request, *args, **kwargs):
        username = self.request.user.username
        if username != settings.ADMIN_USER:
            return HttpResponse(status=400)
        key = json.loads(request.body).get('key')
        switch = get_all_by_table_switch()
        serializer = switch.get(key)
        result = json.dumps(serializer.data)
        return HttpResponse(result)


class delete_data_by_table(ProtectedResourceView):
    permission_classes = [TokenHasReadWriteScope]

    def post(self, request, *args, **kwargs):
        username = self.request.user.username
        if username != settings.ADMIN_USER:
            return HttpResponse(status=400)
        table = json.loads(request.body).get('table')
        selected_list = json.loads(request.body).get('selected')

        delete_by_selected(table=table, selected_list=selected_list)

        serializer = get_all_by_table_switch().get(table)
        result = json.dumps(serializer.data)
        return HttpResponse(result)
 ######


class Validtoken(ProtectedResourceView):
    permission_classes = [TokenHasReadWriteScope]

    def get(self, request, *args, **kwargs):
        return JsonResponse({'name': f'{request.user.username}'})


class upload_files(ProtectedResourceView):
    permission_classes = [TokenHasReadWriteScope]

    def post(self, request, *args, **kwargs):
        upload_files = request.FILES.getlist("files")
        username = request.user.username
        save_path = parse.unquote(request.GET.get('File-Path'))
        # save_path
        # Ex1) /storage/내_드라이브
        # Ex2) /storage/a/b/c
        meta_data = []
        files = check_file_name_is_valid(upload_files)
        result_remaining_size = check_remaining_storage_space(
            upload_files=files, username=username)

        if (result_remaining_size.get('total_file_size') != -1):
            meta_data = save_file(upload_files=files,
                                  username=username, save_path=save_path)
        else:
            return HttpResponse(status=400)

        remaining_size = result_remaining_size.get(
            'used_storage_size') - result_remaining_size.get('total_file_size')
        subject_used_storage_size(
            username=username, remaining_size=remaining_size)
        save_file_path(meta_data=meta_data, username=username)
        return HttpResponse(meta_data, status=200)


class delete_files(ProtectedResourceView):
    def post(self, request, *args, **kwargs):
        body = json.loads(request.body)
        file_list = body.get('file_list')
        path = parse.unquote(body.get('path'))
        username = request.user.username

        meta_data = delete_file(delete_files=file_list,
                                username=username, saved_path=path)
        add_used_storage_size(
            username=username, saved_path=path, meta_data=meta_data)
        meta_set = delete_file_path(username=username, meta_data=meta_data)
        return HttpResponse(json.dumps(meta_set))


class get_storage_size(ProtectedResourceView):
    def get(self, request, *args, **kwargs):
        username = self.request.user.username
        delete_temp_file(username)
        storage_sizes = UserStorage.objects.get(username=username)
        serializer = StorageSizesSerializer(storage_sizes, many=False)
        return JsonResponse(data=serializer.data)


class add_folder(ProtectedResourceView):
    def post(self, request, *args, **kwargs):
        body = json.loads(request.body)
        path = convert_path(parse.unquote(body.get('path')))
        folder_name = parse.unquote(body.get('folder_name'))
        if folder_name == "":
            return HttpResponse(status=400)
        # if path is root: "" + "" + "/"
        # else : "/" + "a/b/c" + "/"
        root_slash = root_path_slash(path)
        converted_path = root_slash + path + '/'
        username = self.request.user.username
        os.mkdir(
            f'{settings.MEDIA_ROOT}/{username}/{path}{root_slash}{folder_name}')
        name = "folder:" + folder_name

        is_ok_files = save_folder_in_files_table(
            username=username, name=name, path=converted_path)
        is_ok_folders = save_folder_in_folders_table(
            username=username, name=name, path=converted_path)
        print(f'{is_ok_files} and {is_ok_folders}')
        return HttpResponse(status=200)


class download_files(ProtectedResourceView):
    def post(self, request, *args, **kwargs):
        body = json.loads(request.body)
        path = convert_path(parse.unquote(body.get('path')))
        username = self.request.user.username
        file_list = body.get('file_list')

        root_slash = root_path_slash(path)
        os.chdir(f'{settings.MEDIA_ROOT}/{username}/{path}{root_slash}')
        fs = FileSystemStorage(location=f'{settings.MEDIA_ROOT}/temp')
        with zipfile.ZipFile(f'{settings.MEDIA_ROOT}/temp/{username}.zip', 'w') as file_list_zip:
            for file in file_list:
                if (file.startswith('folder:')):
                    folder_name = file.split(sep='folder:', maxsplit=1)[1]
                    for (path, dir, files) in os.walk(f'{settings.MEDIA_ROOT}/{username}/{path}{root_slash}{folder_name}'):
                        for file in files:
                            sep_path = path.rsplit(
                                sep=f'{settings.MEDIA_ROOT}/{username}/{path}{root_slash}', maxsplit=1)[1]
                            file_list_zip.write(
                                f'{sep_path}/{file}', compress_type=zipfile.ZIP_DEFLATED)
                else:
                    file_list_zip.write(f'{file}')
            file_list_zip.close()

        response = FileResponse(
            fs.open(f'{username}.zip', 'rb'), as_attachment=True)
        return response


@login_required()
@api_view(['GET'])
def get_file_list_by_path(request, path):
    username = request.user.username
    file_path = path
    file_path = file_path.replace("&", "/")
    # Ex1) 내_드라이브
    # Ex2) a%b%c => a/b/c
    if (file_path == '내_드라이브'):
        # /
        file_path = "/"
    else:
        # /a/b/c/
        file_path = '/'+file_path + '/'
    file_list = File.objects.filter(file_path=file_path, file_owner=username)
    serializer = FileListSerializer(file_list, many=True)
    return Response(serializer.data)


@login_required()
def secret_page(request, *args, **kwargs):
    return HttpResponse('Secret contents!', status=200)
