from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, EmailActivation
from .forms import UserChangeForm, UserCreationForm


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'password', 'full_name', 'date_of_birth',
                    'country', 'address', 'phone_number', 'image', 'is_admin')
    list_filter = ('is_admin', )
    fieldsets = (
        ('Identity', {
            'fields': ('email', 'password')
        }),
        ('Personal info', {
            'fields': ('full_name', 'date_of_birth', 'country', 'address',
                       'phone_number', 'image')
        }),
        ('Permissions', {
            'fields': ('is_admin', )
        }),
        ('Access', {
            'fields': ('is_active', )
        }),
    )
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = ((None, {
        'classes': ('wide', ),
        'fields': ('email', 'full_name', 'date_of_birth', 'country', 'address',
                   'phone_number', 'image', 'password1', 'password2')
    }), )
    search_fields = ('email', )
    ordering = (
        'full_name',
        'email',
        'phone_number',
        'date_of_birth',
        'country',
        'address',
        'image',
    )
    filter_horizontal = ()


# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(EmailActivation)

# since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)