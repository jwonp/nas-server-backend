
from django.contrib import admin
from django.urls import path
from django.conf.urls import  include
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('admin/logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'), #new
    path('admin/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'), #new
    # path('admin/', admin.site.urls),
    path('users/',include('users.urls')),
    path('', include('test_rest_api.urls')),
]
