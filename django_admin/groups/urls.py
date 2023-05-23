from django.urls import path
from .views import ServerName,GetServerName
# UserListView,
urlpatterns = [
    # path('users/', UserListView.as_view(), name='user-list'),
    path('serverName/', ServerName.as_view(), name='server-Name'),

        path('servers/', GetServerName.as_view(), name='servers'),

    
]