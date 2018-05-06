from django.shortcuts import redirect, render

from user_profiles.utils import is_admin


def home(request):
    """ Redirect logged in users to the appropriate views according
    to their Group, and wether they are logged in or not.

    """
    if is_admin(request.user):
        return redirect('administration:list_clients')
    else:
        return render(request, 'base/home.html')


def base_files(request, filename):
    location = 'base/' + filename
    return render(request, location, {}, content_type='text/plain')
