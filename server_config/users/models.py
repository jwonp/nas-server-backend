from django.contrib.auth.models import AbstractUser
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from django.db import models

class UserStorage(models.Model):
    permission_classes = [TokenHasReadWriteScope]
    username = models.CharField(db_column='username',max_length=150,primary_key=True)
    tier = models.SmallIntegerField(db_column='tier')
    max_storage_size = models.FloatField(db_column='max_storage_size')
    used_storage_size = models.FloatField(db_column='used_storage_size')

    class Meta:
        managed = True
        db_table = 'user_storage'
        
class File(models.Model):
    file_id = models.BigAutoField(primary_key=True)
    file_name = models.CharField(db_column='file_name',max_length=100) 
    file_path = models.CharField(db_column='file_path',max_length=300 ) 
    file_upload_date = models.DateTimeField(db_column='file_upload_date')
    file_owner = models.CharField(db_column="file_owner", max_length=150)
    file_size = models.BigIntegerField(db_column='file_size', default=0)
    is_favorite = models.BooleanField(db_column='is_favorite', default=False)
    class Meta:
        unique_together=(('file_name','file_path','file_owner'))
        managed = True
        db_table = 'files'
        
class Folder(models.Model):
    folder_id = models.BigAutoField(primary_key=True)
    folder_name = models.CharField(db_column='folder_name',max_length=100 ) 
    base_path = models.CharField(db_column='base_path',max_length=300 )
    owner = models.CharField(db_column="owner", max_length=150 )
    is_favorite = models.BooleanField(db_column='is_favorite', default=False)
    class Meta:
        unique_together=(('folder_name','base_path','owner'))
        managed = True
        db_table = 'folders'
                
class User(AbstractUser):
    pass
