from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST

from .models import Contact, Group
from .forms import ContactForm, GroupForm, ContactSearchForm
from datetime import date, timedelta

@login_required
def dashboard(request):
    # Statistiques
    total_contacts = Contact.objects.filter(user=request.user, is_deleted=False).count()
    favorite_contacts = Contact.objects.filter(user=request.user, is_favorite=True, is_deleted=False).count()
    deleted_contacts = Contact.objects.filter(user=request.user, is_deleted=True).count()
    
    # Anniversaires à venir (30 jours)
    today = date.today()
    thirty_days_later = today + timedelta(days=30)
    
    upcoming_birthdays = []
    contacts_with_birthdays = Contact.objects.filter(
        user=request.user, 
        is_deleted=False,
        birth_date__isnull=False
    )
    
    for contact in contacts_with_birthdays:
        days = contact.days_until_birthday()
        if days is not None and days <= 30:
            upcoming_birthdays.append({
                'contact': contact,
                'days': days
            })
    
    # Trier par nombre de jours
    upcoming_birthdays.sort(key=lambda x: x['days'])
    
    # Récents contacts
    recent_contacts = Contact.objects.filter(
        user=request.user, 
        is_deleted=False
    ).order_by('-updated_at')[:5]
    
    context = {
        'total_contacts': total_contacts,
        'favorite_contacts': favorite_contacts,
        'deleted_contacts': deleted_contacts,
        'upcoming_birthdays': upcoming_birthdays,
        'recent_contacts': recent_contacts,
    }
    
    return render(request, 'contacts/dashboard.html', context)

@login_required
def contact_list(request):
    contacts = Contact.objects.filter(user=request.user, is_deleted=False)
    form = ContactSearchForm(request.GET, user=request.user)
    
    if form.is_valid():
        search_query = form.cleaned_data.get('search', '')
        group_filter = form.cleaned_data.get('group')
        favorites_only = form.cleaned_data.get('favorites_only')
        
        if search_query:
            contacts = contacts.filter(
                Q(first_name__icontains=search_query) | 
                Q(last_name__icontains=search_query) | 
                Q(email__icontains=search_query) |
                Q(phone_number__icontains=search_query)
            )
        
        if group_filter:
            contacts = contacts.filter(groups=group_filter)
            
        if favorites_only:
            contacts = contacts.filter(is_favorite=True)
    
    # Pagination
    paginator = Paginator(contacts, 10)  # 10 contacts par page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'form': form,
    }
    
    return render(request, 'contacts/contact_list.html', context)

@login_required
def contact_detail(request, pk):
    contact = get_object_or_404(Contact, pk=pk, user=request.user)
    return render(request, 'contacts/contact_detail.html', {'contact': contact})

@login_required
def contact_create(request):
    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.user = request.user
            contact.save()
            form.save_m2m()  # Pour sauvegarder les relations ManyToMany
            messages.success(request, 'Contact créé avec succès!')
            return redirect('contact_detail', pk=contact.pk)
    else:
        form = ContactForm(user=request.user)
    
    return render(request, 'contacts/contact_form.html', {'form': form, 'title': 'Ajouter un contact'})

@login_required
def contact_update(request, pk):
    contact = get_object_or_404(Contact, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES, instance=contact, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Contact modifié avec succès!')
            return redirect('contact_detail', pk=contact.pk)
    else:
        form = ContactForm(instance=contact, user=request.user)
    
    return render(request, 'contacts/contact_form.html', {
        'form': form, 
        'contact': contact,
        'title': 'Modifier le contact'
    })

@login_required
def contact_delete(request, pk):
    contact = get_object_or_404(Contact, pk=pk, user=request.user)
    
    if request.method == 'POST':
        contact.is_deleted = True
        contact.save()
        messages.success(request, 'Contact déplacé dans la corbeille.')
        return redirect('contact_list')
    
    return render(request, 'contacts/contact_confirm_delete.html', {'contact': contact})

@login_required
def trash(request):
    deleted_contacts = Contact.objects.filter(user=request.user, is_deleted=True)
    
    # Pagination
    paginator = Paginator(deleted_contacts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'contacts/trash.html', {'page_obj': page_obj})

@login_required
def restore_contact(request, pk):
    contact = get_object_or_404(Contact, pk=pk, user=request.user, is_deleted=True)
    
    if request.method == 'POST':
        contact.is_deleted = False
        contact.save()
        messages.success(request, 'Contact restauré avec succès.')
        return redirect('trash')
    
    return render(request, 'contacts/contact_restore.html', {'contact': contact})

@login_required
def permanent_delete(request, pk):
    contact = get_object_or_404(Contact, pk=pk, user=request.user, is_deleted=True)
    
    if request.method == 'POST':
        contact.delete()
        messages.success(request, 'Contact supprimé définitivement.')
        return redirect('trash')
    
    return render(request, 'contacts/contact_permanent_delete.html', {'contact': contact})

@login_required
@require_POST
def toggle_favorite(request, pk):
    contact = get_object_or_404(Contact, pk=pk, user=request.user)
    contact.is_favorite = not contact.is_favorite
    contact.save()
    
    return JsonResponse({
        'status': 'success',
        'is_favorite': contact.is_favorite
    })

@login_required
def group_list(request):
    groups = Group.objects.filter(user=request.user)
    
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.user = request.user
            group.save()
            messages.success(request, 'Groupe créé avec succès!')
            return redirect('group_list')
    else:
        form = GroupForm()
    
    return render(request, 'contacts/group_list.html', {
        'groups': groups,
        'form': form
    })

@login_required
def group_detail(request, pk):
    group = get_object_or_404(Group, pk=pk, user=request.user)
    contacts = Contact.objects.filter(user=request.user, groups=group, is_deleted=False)
    
    # Pagination
    paginator = Paginator(contacts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'contacts/group_detail.html', {
        'group': group,
        'page_obj': page_obj
    })

@login_required
def group_update(request, pk):
    group = get_object_or_404(Group, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = GroupForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            messages.success(request, 'Groupe modifié avec succès!')
            return redirect('group_list')
    else:
        form = GroupForm(instance=group)
    
    return render(request, 'contacts/group_form.html', {
        'form': form,
        'group': group
    })

@login_required
def group_delete(request, pk):
    group = get_object_or_404(Group, pk=pk, user=request.user)
    
    if request.method == 'POST':
        group.delete()
        messages.success(request, 'Groupe supprimé avec succès.')
        return redirect('group_list')
    
    return render(request, 'contacts/group_confirm_delete.html', {'group': group})

@login_required
def favorites(request):
    favorite_contacts = Contact.objects.filter(user=request.user, is_favorite=True, is_deleted=False)
    
    # Pagination
    paginator = Paginator(favorite_contacts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'contacts/favorites.html', {'page_obj': page_obj})
