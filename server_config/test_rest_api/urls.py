from django.urls import path
from . import views
app_name = 'test_rest_api'
urlpatterns = [
    path('getfolders/', views.getFolders, name='getfolders'),
    path('register/', views.register, name='register'),
    path('getuser/', views.getUser, name='getuser'),
]
