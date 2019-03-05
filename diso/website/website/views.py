# redirect users to the login page

from django.shortcuts import redirect


def login_redirect(request):
    return redirect('/account/login')
