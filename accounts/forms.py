from django import forms
#from django.contrib.auth.models import User

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