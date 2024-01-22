from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'date_of_birth',
                  'can_be_contacted', 'can_data_be_shared']

    # Ajoutez des widgets pour les champs booléens
    can_be_contacted = forms.BooleanField(initial=True, required=False, widget=forms.CheckboxInput())
    can_data_be_shared = forms.BooleanField(initial=True, required=False, widget=forms.CheckboxInput())