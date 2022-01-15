from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from .models import User
from django import forms

class RegisterUserForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        
    def __init__(self, *args, **kwargs):
        super(RegisterUserForm, self).__init__(*args, **kwargs)
        
        self.fields['username'].label = "Usuário"
        self.fields['email'].label = "E-mail"
        self.fields['first_name'].label = "Nome"
        self.fields['last_name'].label = "Sobrenome"
        self.fields['password1'].label = "Senha"
        self.fields['password2'].label = "Confirmar senha"

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

class EditUserForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']
        
    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        
        self.fields['username'].label = "Usuário"
        self.fields['email'].label = "E-mail"
        self.fields['first_name'].label = "Nome"
        self.fields['last_name'].label = "Sobrenome"
        self.fields['password'].label = "Senha"

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

        self.fields['password'].widget = forms.HiddenInput()

class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(label='Senha atual', widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}))
    new_password1 = forms.CharField(label='Nova senha', widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}))
    new_password2 = forms.CharField(label='Confirmar nova senha', widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}))

    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']