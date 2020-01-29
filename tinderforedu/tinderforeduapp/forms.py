from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, help_text='Last Name')
    last_name = forms.CharField(max_length=100, help_text='Last Name')
    college = forms.CharField(max_length=100, help_text='College')
    email = forms.EmailField(max_length=150, help_text='Email')
    age = forms.CharField(max_length=10, help_text='Age')


    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name', 'age',
'email', 'college', )