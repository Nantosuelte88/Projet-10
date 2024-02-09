from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class UserRegistrationForm(UserCreationForm):
    can_be_contacted = forms.BooleanField(initial=False, required=False, widget=forms.CheckboxInput())
    can_data_be_shared = forms.BooleanField(initial=False, required=False, widget=forms.CheckboxInput())

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'date_of_birth',
                  'can_be_contacted', 'can_data_be_shared']
