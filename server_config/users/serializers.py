from rest_framework import serializers
from .models import File, User, UserStorage,Folder
# first we define the serializers
class UserStorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserStorage
        fields = '__all__'
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        
class UsedStorageSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserStorage
        fields = ['used_storage_size']
        
class StorageSizesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserStorage
        fields = ['max_storage_size','used_storage_size']
        
class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['file_name','file_path','file_upload_date','file_owner','file_size']
        
class FileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['file_name','file_upload_date','file_size']
        
class FolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = '__all__'
# class GroupSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Group
#         fields = ("name", )