from rest_framework import serializers
from .models import File, UserStorage
# first we define the serializers
class UserStorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserStorage
        fields = '__all__'

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'
# class GroupSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Group
#         fields = ("name", )