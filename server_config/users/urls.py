import oauth2_provider.views as oauth2_views
from django.urls import path, include
from django.conf import settings
from .views import ApiEndpoint, Closedpoint, Validtoken,secret_page,Refreshtoken,upload_files

# OAuth2 provider endpoints
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
    # OAuth 2 endpoints:
    # need to pass in a tuple of the endpoints as well as the app's name
    # because the app_name attribute is not set in the included module
    path('o/', include((oauth2_endpoint_views, 'oauth2_provider'), namespace="oauth2_provider")),
    path('uploadfiles/', upload_files.as_view()),
    path('validtoken/',Validtoken.as_view()),
    path('refreshtoken/',Refreshtoken.as_view()),
    path('api/hello/', ApiEndpoint.as_view()),  # an example resource endpoint
    path('api/test/', Closedpoint.as_view()),   
    path('secret/', secret_page, name='secret'),
]