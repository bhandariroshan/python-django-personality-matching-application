from allauth.account.forms import SignupForm
from django import forms
from .models import UserProfile


class MySignupForm(SignupForm):
    model = UserProfile

    class Meta:
        fields = [
            'name',
            'username',
            'email',
            'age',
            'password1',
            'password2',
            'signup_type'
        ]

    choice_dropdown = [(1, 'Girls'), (2, 'Role Model')]

    name = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'label': 'Name',
                'class': u'form-control stored',
                'placeholder': u'Enter Full Name'
            }
        )
    )
    username = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'label': 'Username',
                'class': u'form-control stored',
                'placeholder': u'Username'
            }
        )
    )
    email = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'type': 'email',
                'label': 'Email',
                'class': u'form-control stored',
                'placeholder': u'Enter Email'
            }
        )
    )
    password1 = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'type': 'password',
                'label': 'Password',
                'class': u'form-control stored',
                'placeholder': u'Password'
            }
        )
    )
    password2 = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'type': 'password',
                'label': 'Password Again',
                'class': u'form-control stored',
                'placeholder': u'Re-enter Password'
            }
        )
    )
    age = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'type': 'number',
                'label': 'Age',
                'class': u'form-control stored',
                'placeholder': u'Age eg: 30'
            }
        )
    )
    signup_type = forms.ChoiceField(
        required='True',
        widget=forms.Select(
            attrs={
                'max-length': 4,
                'class': 'form-control stored form-date',
                'placeholder': u'Signup as'
            }),
        choices=choice_dropdown
    )


    def clean_name(self):
        if self.cleaned_data["name"]:
            return str(self.cleaned_data.get("name"))

    def clean_signup_type(self):
        if self.cleaned_data["signup_type"]:
            return int(self.cleaned_data.get("signup_type"))

    def clean_age(self):
        if self.cleaned_data["age"]:
            return int(self.cleaned_data.get("age"))
