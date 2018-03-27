from django import forms

class AccountSignupForm(forms.Form):
    email = forms.CharField(required=True, label="Email", max_length=30)
    name = forms.CharField(required=True, label="Name", max_length=30)
    username = forms.CharField(required=True, label="Username", max_length=30)	
    password = forms.CharField(required=True, label='Password', max_length=30, widget=forms.PasswordInput())

class AccountLoginForm(forms.Form):
    email = forms.CharField(required=True, label="Email", max_length=30)
    password = forms.CharField(required=True, label='Password', max_length=30, widget=forms.PasswordInput())
