
from django.contrib import admin
from django.urls import path
from django.conf.urls import  include
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/',include('users.urls')),
    #debug
    path('__debug__/', include('debug_toolbar.urls')),
    path('', include('test_rest_api.urls')),
]
