from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from . import services


# Authentication
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return HttpResponseRedirect(reverse("home"))
        else:
            return render(request, "main/login.html", {
                "message": "Invalid user"
            })

    return render(request, 'main/login.html')


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))


@login_required
def home(request):
    return render(request, "main/home.html")

@login_required
def show_meal(request):
    if request.method == "POST":
        meal_type = request.POST.get('meal_type')
        cuisine = request.POST.get('cuisine')
        exclude = request.POST.get('exclude')
        callories = request.POST.get('kcal')

    # Pass to Gemini
    meal_data = "test" # Get the data/json
    

    return render(request, "main/showmeal.html", {
        'data': meal_data
    })


@login_required
def history(request):
    return render(request, "main/history.html")