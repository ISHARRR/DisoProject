from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.core.exceptions import ValidationError
from calendar import HTMLCalendar
import re


# Create your models here.
from django.urls import reverse


class UserProfile(models.Model):
    # linking to built in user model
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # twitter username
    twitter_username = models.CharField(max_length=50)

    def __str__(self):
        return self.user.username


# creating the user profile when a user is created
def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=kwargs['instance'])


post_save.connect(create_profile, sender=User)


class Table(models.Model):
    seats = models.PositiveIntegerField()
    available = models.BooleanField(default=True)

    def as_json(self):
        return dict(
            id=self.id,
            seats=self.seats,
            available=self.available
        )

    def __str__(self):
        return str(self.id)


class Reservation(models.Model):
    table = models.ForeignKey('Table', on_delete=models.CASCADE)
    customer = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
    date = models.DateField(help_text='Date of booking')
    start_time = models.TimeField(help_text='Starting Time')
    finish_time = models.TimeField(help_text='Finishing Time')

    def __str__(self):
        return str(self.id)

    @staticmethod
    def check_overlap(fixed_start, fixed_end, new_start, new_end):
        overlap = False
        if new_start == fixed_end or new_end == fixed_start:  # edge case
            overlap = False
        elif (fixed_start <= new_start <= fixed_end) or (fixed_start <= new_end <= fixed_end):  # innner limits
            overlap = True
        elif new_start <= fixed_start and new_end >= fixed_end:  # outter limits
            overlap = True

        return overlap

    def get_absolute_url(self):
        url = reverse('admin:%s_%s_change' % (self._meta.app_label, self._meta.model_name), args=[self.id])
        return u'<a href="%s">%s</a>' % (url, str(self.start_time))

    def clean(self):
        if self.finish_time <= self.start_time:
            raise ValidationError('Ending times must be after starting times')

        reservations = Reservation.objects.filter(date=self.date)
        if reservations.exists():
            for reservation in reservations:
                if self.check_overlap(reservation.start_time, reservation.finish_time, self.start_time, self.finish_time):
                    raise ValidationError(
                        'There is an overlap with another booking: ' + str(reservation.day) + ', ' + str(
                            reservation.start_time) + '-' + str(reservation.finish_time))
