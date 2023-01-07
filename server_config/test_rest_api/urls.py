
from django.contrib import admin
from django.urls import path
from django.conf.urls import  include

from . import views
urlpatterns = [
    # path('', views.index, name='index'),
    # path('viewjson/', views.viewjson, name='viewjson'),

    path('getstoragesize/', views.getStorageSize, name='getstoragesize'),
    path('getfolders/', views.getFolders, name='getfolders'),
    path('authorizationview/',views.authorizationview, name='authorizationview'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('submitlogin/', views.submitLogin, name='submitlogin'),
    path('getuser/', views.getUser, name='getuser'),
    # path('boardlist/', views.boardList, name='boardlist'),
    # path('boardview/<str:pk>/', views.boardView, name='boardview'),
    # path('boardinsert/', views.boardInsert, name='boardinsert'),
    # path('boardupdate/<str:pk>/', views.boardUpdate, name='boardupdate'),
    # path('boarddelete/<str:pk>/', views.boardDelete, name='boarddelete'),
]

