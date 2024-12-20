from django.contrib.auth import login, logout
from django.shortcuts import render, redirect

from auth_user.forms import RegisterForm, LoginForm


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if not form.is_valid():
            return render(request, "register.html", {"form": form})

        customer = form.save()
        login(request, customer)

        return redirect("/")

    form = RegisterForm()
    return render(request, "register.html", {"form": form})

def logout_view(request):
    if request.method == "POST":
        logout(request)

        return redirect("/")

    return redirect("/404")

