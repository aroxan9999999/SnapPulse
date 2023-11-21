from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text=_('Required. Enter a valid email address.'))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = _('Username')
        self.fields['email'].widget.attrs['placeholder'] = _('Email')
        self.fields['password1'].widget.attrs['placeholder'] = _('Password')
        self.fields['password2'].widget.attrs['placeholder'] = _('Confirm Password')
        self.fields['username'].help_text = _('A unique username to identify you.')
        self.fields['email'].help_text = _('A valid email address.')
        self.fields['password1'].help_text = _('Make sure your password is strong.')
        self.fields['password2'].help_text = _('Enter the same password as before for verification.')

        self.fields['username'].error_messages = {
            'unique': _("This username is already taken."),
            'invalid': _("This username contains invalid characters."),
        }
        self.fields['email'].error_messages = {
            'unique': _("This email is already in use."),
            'invalid': _("Enter a valid email address."),
        }
        self.fields['password2'].error_messages = {
            'password_mismatch': _("The two password fields didn’t match."),
        }

        for fieldname in ['username', 'email', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

        for field in self.fields.values():
            field.error_messages = {'required': _("This field is required.")}
