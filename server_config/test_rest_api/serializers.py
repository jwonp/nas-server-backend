from rest_framework import serializers
from .models import Board,File

class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = '__all__'

class UploadSerializer(serializers.Serializer):
    file_uploaded = serializers.FileField()
    class Meta:
        fields = ['file_uploaded']

        