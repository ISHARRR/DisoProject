from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.urls import reverse_lazy

from .models import Reservation
from django.views.generic.edit import DeleteView


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
        # user.first_name = self.cleaned_data['first_name']
        # user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user

    def clean_username(self):
        username = self.cleaned_data.get('username')
        queryset = User.objects.filter(username=username)
        if queryset.exists():
            raise forms.ValidationError("Username is already taken")
        return username


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


class MakeReservationFrom(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = [
            'table',
            'customer',
            'date',
            'start_time',
            'finish_time',
        ]

    def save(self, commit=True):
        reservation = super(MakeReservationFrom, self).save(commit=False)
        reservation.table = self.cleaned_data['table']
        reservation.customer = self.cleaned_data['customer']
        reservation.date = self.cleaned_data['date']
        reservation.start_time = self.cleaned_data['start_time']
        reservation.finish_time = self.cleaned_data['finish_time']

        if commit:
            reservation.save()

        return reservation


class DeleteReservationForm(forms.Form):
    enter_reservation_id = forms.IntegerField(min_value=1)
