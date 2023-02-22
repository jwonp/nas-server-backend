import datetime
from urllib import parse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .models import UserStorage,File
from .serializers import FolderSerializer, UserStorageSerializer,UsedStorageSizeSerializer,FileSerializer
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
    path = convert_path(save_path)  
    sub_path = f'{username}/{path}'
    print("sub path is " ,sub_path)
    fs = FileSystemStorage(location=f'{settings.MEDIA_ROOT}/{sub_path}')
    result_meta_data = []
    
    for item in upload_files:
        file_name = fs.save(item.name, item)
        file_path = fs.path(file_name)
        file_size = fs.size(file_name)
        file_path_list = file_path.split('/')
        username_index = file_path_list.index(username)+1
        file_path_list = file_path_list[username_index:-1]
        file_path = "/".join(file_path_list)+'/'
        
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
        print(item.get('name'))
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
    path = convert_path(saved_path) +'/'
    sub_path = f'{username}/{path}'
    meta_data = []
    location = f'{settings.MEDIA_ROOT}/{sub_path}'
    print("location",location)
    fs = FileSystemStorage(location=location)
    for file_name in delete_files:
        base_path = f'{settings.MEDIA_ROOT}/{username}/'
        print('delete_file base_path is ', base_path)
        file_path = location.split(sep=base_path,maxsplit=1)[1]
        print('delete_file file_path is ', file_path.split(sep=file_name,maxsplit=1)[0])
        if(file_path == ''):
            file_path = '/'
        # print(base_path)
        file_meta = {
            'name':file_name,
            'path':file_path,
            'size':fs.size(file_name)}
        meta_data.append(file_meta)
        fs.delete(file_name)
    print("meta_data is ")
    print(meta_data)
    return meta_data



def add_used_storage_size(username,meta_data):
    total_size = 0
    for item in meta_data:
        total_size += item.get('size')
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

def delete_file_path(username, meta_data):
    for item in meta_data:
        file = File.objects.get(file_owner=username, file_name = item.get('name'), file_path = item.get('path'))
        if file:
            file.delete()
    
# views > add_folder
def save_folder_in_files_table(username,name,path):
    print(f'{username} and {name} and {path}')
    serializer = FileSerializer(data={
            'file_name':name,
            'file_path':path,
            'file_upload_date':datetime.datetime.now(),
            'file_owner':username,
            'file_size':-1
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
    print(f'before {path}')
    if (path == "/storage"):
        path = path + '/내_드라이브'
    print(f'after {path}')
    base_path = '내_드라이브'
    
    splited_path = path.split(sep='/',maxsplit=2)[2]
    print('splited_path is ', splited_path)
    if(base_path == splited_path):
        result = ""
    else:
        result = splited_path
    return result