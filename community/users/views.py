from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegisterUserForm, EditUserForm, ChangePasswordForm
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("my_site:index")
        else:
            messages.error(request, "Credenciais inválidas!")
            return redirect('users:login_user')
    else:
        return render(request, 'users/login.html')

def logout_user(request):
    logout(request)
    return redirect('users:login_user')

def register_user(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)

            return redirect('my_site:index')
    else:
        form = RegisterUserForm()
    
    return render(request, 'users/register.html', {'form': form})

@login_required
def edit_user(request):
    if request.method == 'POST':
        form = EditUserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Usuário com sucesso!")
            return redirect('users:edit_user')
    else:
        form = EditUserForm(instance=request.user)
    
    return render(request, 'users/edit.html', {'form': form})

class ChangePasswordView(PasswordChangeView):
    form_class = ChangePasswordForm
    success_url = reverse_lazy('users:change_passoword_success')

def change_passoword_success(request):
    messages.success(request, "Senha alterada com sucesso!")
    return redirect('users:edit_user')
