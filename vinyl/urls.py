from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

app_name = 'vinyl'

urlpatterns = [
    path('', views.home, name='home'),
    path('collection/', views.vinyl_list, name='vinyl_list'),
    path('statistics/', views.statistics, name='statistics'),
    path('collection/add', views.add_record, name='add_record'),
    path('collection/<int:record_id>/edit/', views.edit_record, name='edit_record'),
    path('collection/<int:record_id>/delete/', views.delete_record, name='delete_record'),
    path('login/', auth_views.LoginView.as_view(
        template_name='vinyl/login.html',
        redirect_authenticated_user=True,
        next_page='vinyl:home'
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(
        next_page='vinyl:home'
    ), name='logout'),
    path('register/', views.register, name='register')
]