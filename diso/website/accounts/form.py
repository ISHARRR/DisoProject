from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


# registration form inherited from the default django UserCreationForm
class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    username = forms.CharField(max_length=50, required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
        )


# checking inputs before committing them to the database
def save(self, commit=True):
    user = super(RegistrationForm, self).save(commit=False)
    user.username = self.cleaned_data['username']
    user.first_name = self.cleaned_data['first_name']
    user.last_name = self.cleaned_data['last_name']
    user.twitter_username = self.cleaned_data['twitter_username']
    user.email = self.cleaned_data['email']

    if commit:
        user.save()

    return user


# edit registration form inherited from the default django UserChangeForm
# listed fields that are editable by the user
class EditProfileForm(UserChangeForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'password'
            )


