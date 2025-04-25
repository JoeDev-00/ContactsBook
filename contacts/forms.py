from django import forms
from .models import Contact, Group
from django.core.exceptions import ValidationError

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'address', 
                  'avatar', 'birth_date', 'notes', 'is_favorite', 'groups']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
            'address': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ContactForm, self).__init__(*args, **kwargs)
        
        if user:
            self.fields['groups'].queryset = Group.objects.filter(user=user)
            
        # Ajouter des classes pour le style
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field_name == 'is_favorite':
                field.widget.attrs['class'] = 'form-check-input'

    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get('first_name', '').strip()
        last_name = cleaned_data.get('last_name', '').strip()
        
        if not first_name and not last_name:
            raise ValidationError("Le prénom ou le nom doit être renseigné.")
        
        return cleaned_data

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name']
        
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(GroupForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'form-control'
    
    def clean_name(self):
        name = self.cleaned_data['name']
        if self.user and not self.instance.pk:  # Si c'est un nouveau groupe
            if Group.objects.filter(name=name, user=self.user).exists():
                raise forms.ValidationError(f'Le groupe "{name}" existe déjà.')
        return name

class ContactSearchForm(forms.Form):
    search = forms.CharField(
        required=False, 
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Rechercher un contact...'
        })
    )
    group = forms.ModelChoiceField(
        queryset=Group.objects.none(),
        required=False,
        empty_label="Tous les groupes",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    favorites_only = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ContactSearchForm, self).__init__(*args, **kwargs)
        
        if user:
            self.fields['group'].queryset = Group.objects.filter(user=user)
