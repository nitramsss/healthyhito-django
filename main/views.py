from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from .models import User

from . import services


# Authentication
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        context = {
            "header": False,
            "message": "Invalid user"
        }

        if user:
            login(request, user)
            return HttpResponseRedirect(reverse("home"))
        else:
            return render(request, "main/login.html", context)

    return render(request, 'main/login.html', {
        "login": True
    })


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))


def signup_view(request):
    if request.method == "POST":
        password=request.POST.get("password")
        confirm_password=request.POST.get("confirm_password")

        context = {
            "header": False, 
            "message": "Password unmatched",
        }

        if password != confirm_password:
            return render(request, 'main/signup.html', context)

        user = User.objects.create(
            username=request.POST.get("username"),
            password=make_password(password),
            first_name=request.POST.get("fname"),
            last_name=request.POST.get("lname"),
        )
        user.save()
        return HttpResponseRedirect(reverse('home'))
    
    return render(request, 'main/signup.html', {
        "signup": True
    })


@login_required
def home(request):
    context = {
        "header": True
    }
    return render(request, "main/home.html", context)

@login_required
def show_meal(request):
    if request.method == "POST":
        meal_type = request.POST.get('meal_type')
        cuisine = request.POST.get('cuisine')
        exclude = request.POST.get('exclude')
        callories = request.POST.get('kcal')

    # Pass to Gemini
    context = {
        "header": True
    } # Get the data/json
    

    return render(request, "main/showmeal.html", context)


@login_required
def history(request):
    context = {
        "header": True
    }
    return render(request, "main/history.html", context)