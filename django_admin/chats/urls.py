from django.urls import path

from . import views
from django.views.generic import RedirectView

urlpatterns = [
    # path('', views.index, name='index'),
            path('<str:room_name>/', views.room, name='room'),
    # path('<str:room_name>/', RedirectView.as_view(url='http://localhost:4200/dashboard/{{room_name}}', permanent=False)),

]