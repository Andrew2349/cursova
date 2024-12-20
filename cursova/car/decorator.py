from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect



def admin_required(view_func):
    def wrapped(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_admin:
            return view_func(request, *args, **kwargs)
        return redirect('/403')
    return wrapped
