from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('migrate/', views.trigger_migrate),

    path('register/', views.register, name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    path('preferences/', views.user_preferences, name='user_preferences'),
    path('sessions/', views.user_sessions, name='user_sessions'),
    path('toggle-theme/', views.toggle_theme, name='toggle_theme'),
    
    # Réinitialisation de mot de passe
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
