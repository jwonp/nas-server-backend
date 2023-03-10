import oauth2_provider.views as oauth2_views
from django.urls import path, include
from django.conf import settings
from . import views
from django.urls import path, include


oauth2_endpoint_views = [
    path('authorize/', oauth2_views.AuthorizationView.as_view(), name="authorize"),
    path('token/', oauth2_views.TokenView.as_view(), name="token"),
    path('revoke-token/', oauth2_views.RevokeTokenView.as_view(), name="revoke-token"),
]

if settings.DEBUG:
    # OAuth2 Application Management endpoints
    oauth2_endpoint_views += [
        path('applications/', oauth2_views.ApplicationList.as_view(), name="list"),
        path('applications/register/',
             oauth2_views.ApplicationRegistration.as_view(), name="register"),
        path('applications/<pk>/',
             oauth2_views.ApplicationDetail.as_view(), name="detail"),
        path('applications/<pk>/delete/',
             oauth2_views.ApplicationDelete.as_view(), name="delete"),
        path('applications/<pk>/update/',
             oauth2_views.ApplicationUpdate.as_view(), name="update"),
    ]

    # OAuth2 Token Management endpoints
    oauth2_endpoint_views += [
        path('authorized-tokens/', oauth2_views.AuthorizedTokensListView.as_view(),
             name="authorized-token-list"),
        path('authorized-tokens/<pk>/delete/', oauth2_views.AuthorizedTokenDeleteView.as_view(),
             name="authorized-token-delete"),
    ]

urlpatterns = [
    path('o/', include((oauth2_endpoint_views, 'oauth2_provider'),
         namespace="oauth2_provider")),
    path('uploadfiles/', views.upload_files.as_view()),
    path('downloadfiles/',  views.download_files.as_view()),
    path('deletefiles/',  views.delete_files.as_view()),
    path('addfolder/',  views.add_folder.as_view()),
    path('getstoragesize/',  views.get_storage_size.as_view()),
    path('getfilelistbypath/<str:path>',  views.get_file_list_by_path),
    path('validtoken/', views.Validtoken.as_view()),
    # admin
    path('checkadmin/', views.check_admin.as_view()),
    path('data/', views.get_all_data.as_view()),
    path('deletedata/', views.delete_data_by_table.as_view()),

]
