from django.contrib.auth.models import AbstractUser
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from django.db import models

class UserStorage(models.Model):
    permission_classes = [TokenHasReadWriteScope]
    username = models.CharField(db_column='username',max_length=150,unique=True)
    # password = models.CharField(db_column='password', max_length=128)
    # email = models.EmailField(db_column='email',max_length=128)
    # first_name = models.CharField(db_column='first_name',max_length=32)
    # last_name = models.CharField(db_column='last_name',max_length=32)
    # is_staff = models.BooleanField(db_column='is_staff', default=False)
    # is_active = models.BooleanField(db_column='is_active',default=False)
    # is_superuser = models.BooleanField(db_column='is_superuser',default=False)
    # last_login = models.DateTimeField(db_column='last_login')
    # date_joined = models.DateTimeField(db_column='date_joined')
    tier = models.SmallIntegerField(db_column='tier')
    max_storage_size = models.FloatField(db_column='max_storage_size')
    used_storage_size = models.FloatField(db_column='used_storage_size')

    class Meta:
        managed = True
        db_table = 'user_storage'
        
class File(models.Model):
    file_name = models.CharField(db_column='file_name',max_length=100) 
    file_path = models.CharField(db_column='file_path',max_length=300) 
    file_upload_date = models.DateTimeField(db_column='file_upload_date')
    file_owner = models.CharField(db_column="file_owner", max_length=150)
    
    class Meta:
        managed = False
        db_table = 'files'
                
class User(AbstractUser):
    pass
