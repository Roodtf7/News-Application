"""
Forms for the users application.
Defines user registration, login, and profile management forms with role-based validation.
"""
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class SimpleUserRegistrationForm(forms.ModelForm):
    """
    Form for registering a new user with basic details.
    """
    password1 = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm password")

    class Meta:
        model = User
        fields = ["username"]
        labels = {
            "username": "Username",
        }
        help_texts = {
            "username": "",
        }


    def clean(self):
        """
        Validate that the two password fields match.
        """
        cleaned_data = super().clean()
        if cleaned_data.get("password1") != cleaned_data.get("password2"):
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data

    def save(self, commit=True):
        """
        Save the user with the correctly hashed password.
        """
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
