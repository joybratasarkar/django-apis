
from django.urls import path, include
from .views import RegisterView, LoginView, UserView, LogoutView, forgotPasswordView, ChangePassword, authenticate_user,confirmRegistration,activate,UserListView
urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('user/', UserView.as_view()),
    path('Logout/', LogoutView.as_view()),
    path('forgotPassword/', forgotPasswordView.as_view()),
    path('ChangePassword/', ChangePassword.as_view()),
    path('authenticate/', authenticate_user.as_view()),
    path('confirmRegistration/', confirmRegistration.as_view(),name='confirmRegistration'),
    path('activate/<token>/', activate.as_view(), name='activate'),
    path('users/', UserListView.as_view(), name='user-list'),


]
