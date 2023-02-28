import datetime

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .models import Folder, User, UserStorage,File
from .serializers import FolderSerializer, UserSerializer, UserStorageSerializer,UsedStorageSizeSerializer,FileSerializer

def get_all_by_table_switch():
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
    
    switch = {
        'files' :get_all_files(),
        'users' : get_all_users(),
        'folders' : get_all_folders(),
        'storages': get_all_storages()
    }
    return switch

def get_delete_by_selected_switch(selected_list):
    def delete_selected_files(selected_list):
        for selected in selected_list: 
            file = File.objects.get(file_name=selected.get('file_name'),file_path=selected.get('file_path'),file_owner=selected.get('file_owner'))
            file.delete()

    def delete_selected_users(selected_list):
        for selected in selected_list:
            user = User.objects.get(id=selected.get('id'))
            user.delete()

    def delete_selected_folders(selected_list):
        for selected in selected_list:
            folder = Folder.objects.get(folder_id=selected.get('folder_id'))
            folder.delete()

    def delete_selected_storages(selected_list):
        for selected in selected_list:
            storage = UserStorage.objects.get(username=selected.get('username'))
            storage.delete()
            
    switch = {
            'files' :delete_selected_files(selected_list),
            'users' : delete_selected_users(selected_list),
            'folders' :delete_selected_folders(selected_list),
            'storages': delete_selected_storages(selected_list)
    }
    return switch

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
    path = convert_path(saved_path)
    sub_path = f'{username}/{path}'
    meta_data = []
    location = f'{settings.MEDIA_ROOT}/{sub_path}'
    
    fs = FileSystemStorage(location=location)
    base_path = f'{settings.MEDIA_ROOT}/{username}/'
    file_path = location.split(sep=base_path,maxsplit=1)[1]
    for file_name in delete_files:
        is_folder = False
        file_size = 0
        if(file_path == ''):
            file_path = '/'
        if("folder:" in file_name):
            is_folder = True
        else:
            file_size = fs.size(file_name)
        # print(base_path)
        
        file_meta = {
            'name':file_name,
            'path':file_path,
            'size':file_size,
            'is_folder': is_folder
            }
        meta_data.append(file_meta)
        if is_folder == False:
            fs.delete(file_name)
        return meta_data



def add_used_storage_size(username,saved_path,meta_data):
    path = convert_path(saved_path) +'/'
    total_size = 0
    for item in meta_data:
        if item.get('is_folder') == False:
            total_size += item.get('size')
            continue;
        
        files_in_folder = File.objects.filter(file_owner=username,file_path__istartswith=path)
        folder_size = 0
        for file in files_in_folder:
            folder_size += file.file_size
        total_size += folder_size

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

def delete_file_path(username, saved_path,meta_data):
    for item in meta_data:
        if item.get('is_folder') == True:
            path = convert_path(saved_path) +'/' + getFolderName(item.get('name')) + '/'
            files = File.objects.filter(file_owner=username,file_path__istartswith=path)
            for file in files:
                if file:
                    file.delete()
        else :
            file = File.objects.get(file_owner=username, file_name = item.get('name'), file_path = item.get('path'))
            if file:
                file.delete()

def getFolderName(name):
    splitedName = name.split(sep=":" ,maxsplit=1)
    if (splitedName[0] == "folder"):
        return splitedName[1];
    return ""

    
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

def delete_temp_file(username):
    location = f'{settings.MEDIA_ROOT}/temp'
    file_name = f'{username}.zip'
    fs = FileSystemStorage(location=location)
    fs.delete(file_name)
