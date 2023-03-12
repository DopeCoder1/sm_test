from django.urls import path
from no_auth_pages import views


urlpatterns = [
    path('', views.index, name='no_auth_page'),
]


