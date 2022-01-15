from django.contrib import admin
from django.contrib.auth import admin as auth_admin

from .forms import RegisterUserForm, EditUserForm
from .models import User

@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    form = EditUserForm
    add_form = RegisterUserForm
    model = User
    fieldset = auth_admin.UserAdmin.fieldsets + (
        ("Campos personalizados", {'fields': (',')}),
    )