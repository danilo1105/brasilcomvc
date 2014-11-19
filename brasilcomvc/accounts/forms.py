# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm


class DeleteUserForm(forms.Form):

    password = forms.CharField(label='Senha', widget=forms.PasswordInput)

    def __init__(self, user, *args, **kwargs):
        super(DeleteUserForm, self).__init__(*args, **kwargs)
        self.user = user

    def clean_password(self):
        password = self.cleaned_data['password']
        if not self.user.check_password(password):
            self.add_error('password', 'Senha inválida')
        return password


class LoginForm(AuthenticationForm):

    # this is named username so we can use Django's login view
    username = forms.EmailField(required=True)


class SignupForm(forms.ModelForm):

    password = forms.CharField(label='Senha', widget=forms.PasswordInput)

    class Meta:
        model = get_user_model()
        fields = ('full_name', 'email',)

    def save(self, **kwargs):
        # Set password from user input
        self.instance.set_password(self.cleaned_data['password'])
        return super(SignupForm, self).save(**kwargs)


class SecuritySettingsForm(PasswordChangeForm):
    pass
