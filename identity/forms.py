from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import get_user_model, authenticate
from .models import User
from django.core.validators import EmailValidator
User = get_user_model()


class DateInput(forms.DateInput):
    input_type = 'date'


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Verify Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'full_name', 'date_of_birth', 'country', 'address',
                  'phone_number')
        # change date from ordinary input to date input
        widgets = {'date_of_birth': DateInput()}

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and (password1 != password2):
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_active = False
        # create a new user hash for activating email.
        if commit:
            user.save()
        return user

    # Add boostrap class called "form-control to each rendered field"
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'full_name', 'date_of_birth', 'country',
                  'address', 'phone_number', 'is_active', 'is_admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserLoginForm(forms.Form):

    email = forms.EmailField(
        max_length=255,
        validators=[
            EmailValidator(
                message="Invalid Email Address", code="invalid_email")
        ])

    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        user_obj = User.objects.filter(email=email).first()
        if not user_obj:
            raise forms.ValidationError("Incorrect username or password.")
        else:
            if not user_obj.check_password(password):
                raise forms.ValidationError("Incorrect username or password.")
            if not user_obj.is_active:
                raise forms.ValidationError(
                    "Please Verify your email address !")
        return super(UserLoginForm, self).clean(*args, **kwargs)

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
