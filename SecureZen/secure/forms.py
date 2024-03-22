# Import necessary modules and classes from Django
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from .models import User

# Custom form for user login, inherits from AuthenticationForm
class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(attrs={"autofocus": True, 'class': 'form-control', 'placeholder': 'Enter your username'})
    )
    # Customize the password field
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password", 'class': 'form-control', 'placeholder': 'Enter your password'})
    )

    # Meta class to associate the form with the User model
    class Meta:
        model = User
        # Specify the fields to be included in the form
        fields = ['username', 'password']

# Custom form for user registration, inherits from Django's built-in UserCreationForm
class UserRegistrationForm(UserCreationForm):
    # Customize additional fields for user registration
    first_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter your first name"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter your last name"}))
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Choose a username"}))
    email = forms.CharField(widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Enter your email"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Enter a password"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Confirm your password"}))

    # Meta class to associate the form with the User model
    class Meta:
        model = User
        # Specify the fields to be included in the form
        fields = ("first_name", "last_name", "username", "email", "password1", "password2")

# Custom form for user profile editing, inherits from Django's built-in UserChangeForm
class ProfileForm(UserChangeForm):
    # Add an image field for the user's profile picture
    image = forms.ImageField(widget=forms.FileInput(attrs={"class": "form-control mt-3"}), required=False)
    # Customize additional fields for profile editing
    first_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter your first name"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter your last name"}))
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Choose a username"}))
    email = forms.CharField(widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Enter your email"}))

    # Meta class to associate the form with the User model
    class Meta:
        model = User
        # Specify the fields to be included in the form
        fields = ("image", "first_name", "last_name", "username", "email")
