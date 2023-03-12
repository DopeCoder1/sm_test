from django.urls import path
from user import views

urlpatterns = [
    path('register/', views.user_register_request, name='register'),
    path('login/', views.LoginUser.as_view(), name='login_request'),
    path('logout/', views.LogoutView.as_view(), name='logout_request'),

    path('user/profile/', views.user_profile_get_request, name='user_profile'),
    path('user/profile/edit/', views.user_profile_edit, name='user_edit'),
]


