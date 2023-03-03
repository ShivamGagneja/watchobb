from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
import re

USER = get_user_model()
Choice_value = [('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')]
pass_hint = """Password must contain at least 8 characters.\n
            Password should not be similar to personal information.\n
            Password can't be entirely numeric.\n
            Use of special characters is recommended."""

class UserCreationForm(forms.ModelForm):
    firstname       = forms.CharField(required   = False, widget=forms.TextInput(attrs={'maxlength':80, 'required':True,'placeholder':'Enter First Name'}))
    lastname        = forms.CharField(required   = False, widget=forms.TextInput(attrs={'maxlength':80, 'required':True, 'placeholder':'Enter Last Name'}))
    date_of_birth   = forms.DateField(required   = False, widget=forms.NumberInput(attrs={'type':'date', 'required': True}))
    gender          = forms.ChoiceField(required = False, choices=Choice_value)
    email           = forms.EmailField(required  = False, widget=forms.EmailInput(attrs={'maxlength':254, 'required': True, 'placeholder':'Enter your Email'}))
    phone           = forms.CharField(required   = False, widget=forms.NumberInput(attrs={'maxlength':10,'minlength':10,'required': True, 'placeholder':'Enter 10 digit Phone Number'}))
    password1       = forms.CharField(required   = False, label="Password", widget=forms.PasswordInput, help_text=pass_hint)
    password2       = forms.CharField(required   = False, label="Confirm Password", widget=forms.PasswordInput)

    class Meta:
        model = USER
        fields = ('firstname','lastname','date_of_birth','gender','email','phone','password1', 'password2')

    def clean_firstname(self):
        firstname = self.cleaned_data.get("firstname")
        if firstname and not re.search("^[a-zA-Z]+$",firstname):
            raise forms.ValidationError('No special characters or numbers allowed')
        return firstname.capitalize()

    def clean_lastname(self):
        lastname = self.cleaned_data.get("lastname")
        if lastname and not re.search("^[a-zA-Z]+$",lastname):
            raise forms.ValidationError('No special characters or numbers allowed')
        return lastname.capitalize()

    def clean_email(self):
        email = self.cleaned_data['email']
        if USER.objects.filter(email=email).exists():
            raise forms.ValidationError('Account Already Exists')
        return email

    def clean_password1(self):
        firstname = self.cleaned_data.get("firstname")
        lastname = self.cleaned_data.get("lastname")
        password1 = self.cleaned_data.get("password1")
        if password1 and len(password1) < 8:
            raise forms.ValidationError("Must contain at least 8 characters")
        elif password1 and (re.search(password1,firstname) or re.search(password1,lastname)):
            raise forms.ValidationError("Password should not be similar to name")
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if len(phone) == 0:
            raise forms.ValidationError("")
        elif len(phone) != 10:
            raise forms.ValidationError("Invalid phone number")
        return phone

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user