# users/decorators.py
from django.shortcuts import redirect
from functools import wraps

def faculty_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'faculty':
            return view_func(request, *args, **kwargs)
        return redirect('home')  # or some "Not Authorized" page
    return wrapper
