from django.urls import path
from .views import UserListView,ServerName,GetServerName

urlpatterns = [
    path('users/', UserListView.as_view(), name='user-list'),
    path('serverName/', ServerName.as_view(), name='server-Name'),

        path('servers/', GetServerName.as_view(), name='servers'),

    
]