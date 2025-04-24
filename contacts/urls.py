from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('contacts/', views.contact_list, name='contact_list'),
    path('contacts/create/', views.contact_create, name='contact_create'),
    path('contacts/<int:pk>/', views.contact_detail, name='contact_detail'),
    path('contacts/<int:pk>/update/', views.contact_update, name='contact_update'),
    path('contacts/<int:pk>/delete/', views.contact_delete, name='contact_delete'),
    path('contacts/<int:pk>/favorite/', views.toggle_favorite, name='toggle_favorite'),
    
    path('trash/', views.trash, name='trash'),
    path('trash/<int:pk>/restore/', views.restore_contact, name='restore_contact'),
    path('trash/<int:pk>/permanent-delete/', views.permanent_delete, name='permanent_delete'),
    
    path('groups/', views.group_list, name='group_list'),
    path('groups/<int:pk>/', views.group_detail, name='group_detail'),
    path('groups/<int:pk>/update/', views.group_update, name='group_update'),
    path('groups/<int:pk>/delete/', views.group_delete, name='group_delete'),
    
    path('favorites/', views.favorites, name='favorites'),
]
