import datetime
import os
import shutil

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .models import Folder, User, UserStorage,File
from .serializers import FolderSerializer, UserSerializer, UserStorageSerializer,UsedStorageSizeSerializer,FileSerializer
def get_all_files():
    file = File.objects.all()
    serializer = FileSerializer(file, many=True)
    return serializer

def get_all_users():
    user = User.objects.all()
    serializer = UserSerializer(user, many=True)
    return serializer

def get_all_folders():
    folder = Folder.objects.all()
    serializer = FolderSerializer(folder, many=True)
    return serializer

def get_all_storages():
    user_storage = UserStorage.objects.all()
    serializer = UserStorageSerializer(user_storage, many=True)
    return serializer

def get_all_by_table_switch():
    switch = {
        'files' :get_all_files(),
        'users' : get_all_users(),
        'folders' : get_all_folders(),
        'storages': get_all_storages()
    }
    return switch

def delete_selected_files(selected_list):
    for selected in selected_list: 
        file = File.objects.get(file_name=selected.get('file_name'),file_path=selected.get('file_path'),file_owner=selected.get('file_owner'))
        file.delete()


def delete_selected_users(selected_list):
    for selected in selected_list:
        user = User.objects.get(username=selected.get('username'))
        user.delete()

def delete_selected_folders(selected_list):
    for selected in selected_list:
        folder = Folder.objects.get(folder_id=selected.get('folder_id'))
        folder.delete()


def delete_selected_storages(selected_list):
    for selected in selected_list:
        storage = UserStorage.objects.get(username=selected.get('username'))
        storage.delete()

        
def delete_by_selected(table,selected_list):
    if table == 'files':
        delete_selected_files(selected_list)
    elif table == 'users':
        delete_selected_users(selected_list)
    elif table == 'folders':  
        delete_selected_folders(selected_list)
    elif table == 'storages':
        delete_selected_storages(selected_list)
    else:
        return


def get_user_id(username):
    user_data = UserStorage.objects.get(id=username)
    serializer = UserStorageSerializer(user_data, many=False)
    return serializer.data

#views > class : upload_files  
def check_file_name_is_valid(upload_files):
    filtered_files = []
    for item in upload_files:
        file_name = item.name
        if ":" in file_name :
            continue
        filtered_files.append(item)
    return filtered_files
def check_remaining_storage_space(upload_files, username):
    total_file_size = 0
    for item in upload_files:
        total_file_size += item.size
    
    user_storage = UserStorage.objects.get(username = username)
    used_storage_size =  UsedStorageSizeSerializer(user_storage, many=False).data.get('used_storage_size')
    
    if (used_storage_size >= total_file_size):
        return {'total_file_size':total_file_size ,'used_storage_size':used_storage_size}
    else:
        return {'total_file_size':-1 ,'used_storage_size':used_storage_size}

def save_file(upload_files,username,save_path):
    # if path is root path: path = ""
    # else: path = "a/b/c"
    path = convert_path(save_path)
    # if path is root path:
    #   sub_path = "username"
    # else:
    #   sub_path = "username/a/b/c"
    sub_path = f'{username}/{path}'
    fs = FileSystemStorage(location=f'{settings.MEDIA_ROOT}/{sub_path}')
    result_meta_data = []
    
    for item in upload_files:
        file_name = fs.save(item.name, item)
        file_path = fs.path(file_name)
        file_size = fs.size(file_name)
        file_path_list = file_path.split('/')
        username_index = file_path_list.index(username)+1
        file_path_list = file_path_list[username_index:-1]
        if len(file_path_list) == 0:
            root_slash = ""
        else:
            root_slash = "/"
        file_path = root_slash + "/".join(file_path_list)+'/'
        
        result_meta_data.append({
            'name':file_name,
            'path':file_path,
            'size':file_size
            })
    
    return result_meta_data
    

def subject_used_storage_size(username,remaining_size):
    user_storage = UserStorage.objects.get(username=username)
    serializer = UserStorageSerializer(instance=user_storage, data={
        'username':user_storage.username,
        'tier':user_storage.tier,
        'max_storage_size':user_storage.max_storage_size,
        'used_storage_size':remaining_size
        })
    if(serializer.is_valid()):
        print("good")
        serializer.save()
    else:
        print("not good")

def save_file_path(meta_data,username):
    for item in meta_data:
        serializer = FileSerializer(data={
            'file_name':item.get('name'),
            'file_path':item.get('path'),
            'file_upload_date':datetime.datetime.now(),
            'file_owner':username,
            'file_size':item.get('size')
            })
        if serializer.is_valid():
            serializer.save()


# views delete_files
def delete_file(delete_files,username,saved_path):
    # if path is root path: path = ""
    # else: path = "a/b/c"
    path = convert_path(saved_path)
    root_slash = root_path_slash(path)
    sub_path = f'{username}{root_slash}{path}'
    meta_data = []
    # if path is root path: 
    #   sub_path = "username"
    #   location = "...MEDIA_ROOT/username"
    # else:
    #   sub_path = "username/a/b/c"
    #   location = "...MEDIA_ROOT/username/a/b/c"
    location = f'{settings.MEDIA_ROOT}/{sub_path}'
    
    fs = FileSystemStorage(location=location)
    # base_path = f'{settings.MEDIA_ROOT}/{username}'
    # if(base_path == location):
    #     splited_location = ""
    # else:
    #     splited_location = location.split(sep=base_path,maxsplit=1)[1]
    
    #file_path = "/" or "/a/b/c/"
    file_path = root_slash + path + '/'
    for file_name in delete_files:
        is_folder = False
        file_size = 0
        name = file_name
        if("folder:" in name):
            is_folder = True
            name = name.split(sep="folder:",maxsplit=1)[1]
            for file in os.scandir(f'{settings.MEDIA_ROOT}/{sub_path}/{name}'):
                file_size+=os.path.getsize(file)
        else:
            file_size = fs.size(name)
        
        file_meta = {
            'name':name,
            'path':file_path,
            'size':file_size,
            'is_folder': is_folder
            }
        meta_data.append(file_meta)
        
        try:
            if is_folder:
                shutil.rmtree(path=f'{settings.MEDIA_ROOT}/{sub_path}/{name}')
            else :
                fs.delete(name)
        except FileNotFoundError:
            print("FileNotFoundError")
            continue
    return meta_data



def add_used_storage_size(username,saved_path,meta_data):
    # path = convert_path(saved_path) +'/'
    total_size = 0
    for item in meta_data:
        total_size += item.get('size')
        # if item.get('is_folder') == False:
            # total_size += item.get('size')
        #     continue;
        
        # files_in_folder = File.objects.filter(file_owner=username,file_path__istartswith=path)
        # folder_size = 0
        # for file in files_in_folder:
        #     folder_size += file.file_size
        # total_size += folder_size

    user_storage = UserStorage.objects.get(username = username)
    used_storage_size = user_storage.used_storage_size + total_size
    serializer = UserStorageSerializer(instance=user_storage,data={
        'username':user_storage.username,
        'tier':user_storage.tier,
        'max_storage_size':user_storage.max_storage_size,
        'used_storage_size':used_storage_size
        })
    if(serializer.is_valid()):
        print("add_used_storage_size is succeeded")
        serializer.save()
    else:
        print("add_used_storage_size is failed")

def delete_file_path(username,meta_data):
    meta_set = []
    for item in meta_data:
        name = item.get('name')
        path = item.get('path')
        if item.get('is_folder') == True:
            # 목포 폴더 내 하위 파일, 폴더 삭제
            files = File.objects.filter(file_owner=username, file_path__startswith=f'{path}{name}/')
            for file in files:
                if file:
                    file.delete()
            folders = Folder.objects.filter(owner=username,base_path__startswith=f'{path}{name}/')
            for folder in folders:
                if folder:
                    folder.delete()
            # 목표 폴더 삭제
            folder = Folder.objects.get(owner=username,folder_name=f'folder:{name}',base_path=path)
            if folder:
                folder.delete()
            file = File.objects.get(file_owner=username, file_name =f'folder:{name}', file_path = path)
            if file:
                file.delete()
        else:
            file = File.objects.get(file_owner=username,file_name =name,file_path =path)
            if file:
                file.delete()
    return meta_set

def getFolderName(name):
    splitedName = name.split(sep=":" ,maxsplit=1)
    if (splitedName[0] == "folder"):
        return splitedName[1];
    return ""

    
# views > add_folder
def save_folder_in_files_table(username,name,path):
    serializer = FileSerializer(data={
            'file_name':name,
            'file_path':path,
            'file_upload_date':datetime.datetime.now(),
            'file_owner':username,
            'file_size':0
    })
    if serializer.is_valid():
        print("save_folder_in_files_table")
        serializer.save()
        return True
    return False

def save_folder_in_folders_table(username,name,path):
    serializer = FolderSerializer(data={
            'folder_name':name,
            'base_path':path,
            'owner':username,
    })
    if serializer.is_valid():
        print("save_folder_in_folders_table")
        serializer.save()
        return True
    return False




# for export 
def convert_path(path):
    base_path = '내_드라이브'
    splited_path = path.split('/storage/',maxsplit=1)[1]
    if(base_path == splited_path):
        result = ""
    else:
        result = splited_path
    return result

def delete_temp_file(username):
    location = f'{settings.MEDIA_ROOT}/temp'
    file_name = f'{username}.zip'
    fs = FileSystemStorage(location=location)
    fs.delete(file_name)

def root_path_slash(path):
    if(path == ""): return ""
    else : return "/"