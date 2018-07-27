from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

# ADDITIONAL_USER_FIELDS = (
#     (None, {'fields': ('name', 'cpf', 'date_of_birth', 'telephone', 'email')}),
# )
#
# class PersonAdmin(UserAdmin):
#     model = Person
#     add_fieldsets = UserAdmin.add_fieldsets + ADDITIONAL_USER_FIELDS
#     fieldsets = UserAdmin.fieldsets + ADDITIONAL_USER_FIELDS

# admin.site.register(User, UserAdmin)
from .models import SystemSettings

admin.site.register(SystemSettings)
