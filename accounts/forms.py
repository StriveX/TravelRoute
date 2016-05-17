from django import forms
from django.contrib.auth.models import User

from .models import UserProfile


class LoginForm(forms.Form):
    username = forms.CharField(
        required=True,
        label=u"User Name",
        error_messages={'required': 'User name required'},
        widget=forms.TextInput(
            attrs={
                'placeholder':u"User name",
            }
        ),
    )
    password = forms.CharField(
        required=True,
        label=u"Password",
        error_messages={'required': u'Password required'},
        widget=forms.PasswordInput(
            attrs={
                'placeholder':u"Password",
            }
        ),
    )

    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError(u"User name and passwrod are required")
        else:
            cleaned_data = super(LoginForm, self).clean()


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website',)