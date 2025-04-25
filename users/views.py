from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.http import JsonResponse

from .forms import CustomUserCreationForm, CustomAuthenticationForm, UserPreferencesForm
from .models import UserSession
from contacts.models import Group
from django.shortcuts import redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import REDIRECT_FIELD_NAME

def guest_required(view_func):
    """
    Décorateur qui permet d'accéder à une vue uniquement si l'utilisateur n'est pas connecté.
    Si l'utilisateur est connecté, il est redirigé vers l'URL spécifiée.
    """
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper

@guest_required
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Créer des groupes par défaut pour l'utilisateur
            default_groups = [
                "Famille",
                "Amis",
                "Travail",
                "Collègues",
                "Importants"
            ]
            
            for group_name in default_groups:
                Group.objects.create(name=group_name, user=user)
            
            login(request, user)
            messages.success(request, "Inscription réussie! Bienvenue dans Répertoire.")
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'registration/login.html'
    
    def form_valid(self, form):
        response = super().form_valid(form)
        
        # Enregistrer la session
        user = self.request.user
        session_key = self.request.session.session_key
        ip_address = self.request.META.get('REMOTE_ADDR')
        user_agent = self.request.META.get('HTTP_USER_AGENT', '')
        
        UserSession.objects.create(
            user=user,
            session_key=session_key,
            ip_address=ip_address,
            user_agent=user_agent
        )
        
        return response

@login_required
def user_preferences(request):
    if request.method == 'POST':
        form = UserPreferencesForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Préférences mises à jour avec succès.")
            return redirect('user_preferences')
    else:
        form = UserPreferencesForm(instance=request.user)
    
    return render(request, 'users/preferences.html', {'form': form})

@login_required
def user_sessions(request):
    sessions = UserSession.objects.filter(user=request.user).order_by('-last_activity')
    return render(request, 'users/sessions.html', {'sessions': sessions})

@login_required
def toggle_theme(request):
    user = request.user
    if user.theme_preference == 'light':
        user.theme_preference = 'dark'
    else:
        user.theme_preference = 'light'
    user.save()
    
    return JsonResponse({
        'status': 'success',
        'theme': user.theme_preference
    })


