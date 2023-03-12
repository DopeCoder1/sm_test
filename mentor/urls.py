from django.urls import path
from mentor import views

urlpatterns = [
    path('mentor_register/', views.m_user_register_request, name='m_register'),
    path('mentor_login/', views.m_LoginUser.as_view(), name='m_login_request'),
    path('mentor_logout/', views.m_LogoutUser.as_view(), name='m_logout_request'),

    path('mentor_user/profile/', views.m_user_profile_get_request, name='m_user_profile'),
    path('mentor_user/profile/edit/', views.m_user_profile_edit, name='m_user_edit'),
    path('mentor/create_exam/', views.add_exam, name="m_create_exam"),
    path('mentor/list_exam/', views.list_exam, name="m_list_exam"),
    # path('mentor/<int:pk>/exam/', views.edit_exam, name="m_edit_exam"),
    # path('mentor/<int:pk>/delete_exam/', views.delete_exam, name="m_delete_exam")
]


