from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('bots/', views.bots_list, name='bots_list'),
    path('bots/<int:bot_id>/', views.bot_detail, name='bot_detail'),
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='landing_page'), name='logout'),
    path('profile/', views.profile, name='profile'),
]