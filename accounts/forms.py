from django import forms
from django.contrib.auth import get_user_model


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control form-control-user",
        "placeholder": "Enter Username",
        "id": "examplelogin"
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-control form-control-user",
        "placeholder": "Enter Password",
        "id": "exampleloginPassword"
    }))


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-control form-control-user",
        "placeholder": "Password",
        "id": "exampleInputPassword"
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-control form-control-user",
        "placeholder": "Repeat Password",
        "id": "exampleRepeatPassword"
    }))

    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={
                "class": "form-control form-control-user",
                "placeholder": "User Name",
                "id": "exampleUserName"
            }),
            'first_name': forms.TextInput(attrs={
                "class": "form-control form-control-user",
                "placeholder": "Name",
                "id": "exampleFirstName"
            }),
            'email': forms.EmailInput(attrs={
                "class": "form-control form-control-user",
                "placeholder": "Email address",
                "id": "email"
            }),
        }
        labels = {
            'username': 'Username',
            'first_name': 'First Name',
            'email': 'Email Address',
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd.get('password') != cd.get('password2'):
            raise forms.ValidationError("Passwords do not match")
        return cd['password2']
