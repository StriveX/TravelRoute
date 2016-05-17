from django import forms
from django.contrib.auth.models import User





class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website',)


class EditRouteForm(forms.Form):
    route_name = forms.CharField(label='Route Name', max_length=30)
    description = forms.CharField(widget=forms.Textarea)
