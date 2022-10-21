from django import forms
from django.forms import CharField
from django.forms import widgets
from .models import Account


class RegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=100)

    phone_number = forms.CharField(max_length=50)

    email = forms.EmailField(max_length=50)

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter password'
    }))

    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm password'
    }))

    class Meta:
        model = Account
        fields = ['username', 'phone_number', 'email', 'password']

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Enter username'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter phone number'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter email'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                'Password does not match!'
            )