import oauth2_provider.views as oauth2_views
from django.urls import path, include
from django.conf import settings
from .views import  Validtoken, add_folder,upload_files,get_file_list_by_path,get_storage_size,delete_files,download_files
from django.urls import path, include
app_name = 'users'

oauth2_endpoint_views = [
    path('authorize/', oauth2_views.AuthorizationView.as_view(), name="authorize"),
    path('token/', oauth2_views.TokenView.as_view(), name="token"),
    path('revoke-token/', oauth2_views.RevokeTokenView.as_view(), name="revoke-token"),
]

if settings.DEBUG:
    # OAuth2 Application Management endpoints
    oauth2_endpoint_views += [
        path('applications/', oauth2_views.ApplicationList.as_view(), name="list"),
        path('applications/register/', oauth2_views.ApplicationRegistration.as_view(), name="register"),
        path('applications/<pk>/', oauth2_views.ApplicationDetail.as_view(), name="detail"),
        path('applications/<pk>/delete/', oauth2_views.ApplicationDelete.as_view(), name="delete"),
        path('applications/<pk>/update/', oauth2_views.ApplicationUpdate.as_view(), name="update"),
    ]

    # OAuth2 Token Management endpoints
    oauth2_endpoint_views += [
        path('authorized-tokens/', oauth2_views.AuthorizedTokensListView.as_view(), name="authorized-token-list"),
        path('authorized-tokens/<pk>/delete/', oauth2_views.AuthorizedTokenDeleteView.as_view(),
            name="authorized-token-delete"),
    ]

urlpatterns = [
    path('o/', include((oauth2_endpoint_views, 'oauth2_provider'), namespace="oauth2_provider")),
    path('uploadfiles/', upload_files.as_view()),
    path('downloadfiles/', download_files.as_view()),
    path('deletefiles/', delete_files.as_view()),
    path('addfolder/', add_folder.as_view()),
    path('getstoragesize/', get_storage_size.as_view()),
    path('getfilelistbypath/<str:path>', get_file_list_by_path),
    path('validtoken/',Validtoken.as_view()),
]