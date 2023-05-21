from django.urls import path

from . import views
from django.views.generic import RedirectView
from .views import UserListView

urlpatterns = [
    path('users/', UserListView.as_view(), name='user-list'),

]