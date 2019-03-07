from django.shortcuts import render, redirect
from accounts.form import RegistrationForm, EditProfileForm, MakeReservationFrom
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .models import Reservation, Table
from django.http import JsonResponse
from django.core import serializers
from django.http import HttpResponse


# Create your views here.

def home(request):
    template_name = 'accounts/home.html'

    # reservations = Reservation.objects.all()
    # args = {'reservations': reservations}
    # return render(request, template_name, args)
    tables = Table.objects.all()
    # tables.refresh_from_db()
    return render(request, template_name, {'tables': tables})


# gets table data as passes it as a json
def update_tables(request):
    table_as_json = serializers.serialize('json', Table.objects.all())
    return HttpResponse(table_as_json, content_type='json')


# using the built in form class to create a new user
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/account')
    else:
        form = RegistrationForm()

        args = {'form': form}
        return render(request, 'accounts/reg_form.html', args)


# displaying user profile info
@login_required()
def view_profile(request):
    args = {'user': request.user}
    return render(request, 'accounts/profile.html', args)


# posting edited profile
@login_required()
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('/account/profile')
    else:
        form = EditProfileForm(instance=request.user)
        args = {'form': form}
        return render(request, 'accounts/edit_profile.html', args)


@login_required()
def view_reservation(request):
    obj = Reservation.objects.get(id=1)
    args = {
        'table': obj.table,
        'customer': obj.customer,
        'date': obj.date,
        'start_time': obj.start_time,
        'finish_time': obj.finish_time,
    }
    return render(request, 'accounts/reservations.html', args)


@login_required()
def make_reservation(request):
    if request.method == 'POST':
        form = MakeReservationFrom(request.POST)
        if form.is_valid():
            form.save()
            args = {'form': form}
            return render(request, 'accounts/make_reservation.html', args)
    else:
        form = MakeReservationFrom()

        args = {'form': form}
        return render(request, 'accounts/reg_form.html', args)


# changing password if old password is known
@login_required()
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('/account/profile')
        else:
            return redirect('change_password')
    else:
        form = PasswordChangeForm(user=request.user)
        args = {'form': form}
        return render(request, 'accounts/change_password.html', args)


