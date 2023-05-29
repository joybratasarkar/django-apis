from django.urls import path
from .views import ServerName,GetServerName,GetAllServerName,AddServerName,GetMessage
# UserListView,
urlpatterns = [
    # path('users/', UserListView.as_view(), name='user-list'),
    path('serverName/', ServerName.as_view(), name='server-Name'),

        path('servers/', GetServerName.as_view(), name='servers'),

            path('allServers/', GetAllServerName.as_view(), name='all-servers'),
        path('GetMessage/', GetMessage.as_view(), name='GetMessage'),
 
]