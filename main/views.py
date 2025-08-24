from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from .models import User, UserProfile
import json

from .services import gemini_api


# Authentication
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        context = {
            "login": True,
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

        age=int(request.POST.get("age"))
        weight =float(request.POST.get("weight"))
        height = float(request.POST.get("height"))
        bmi = float((weight)/(height**2))
        allergies="test"

        user_profile = UserProfile.objects.create(
            user=user,
            age=age,
            weight=weight,
            height=height,
            bmi=bmi,
            allergies=allergies
        )

        user.save()
        user_profile.save()

        return HttpResponseRedirect(reverse('home'))
    
    return render(request, 'main/signup.html', {
        "signup": True
    })


@login_required
def home(request):
    context = {
        "header": True,
    }
    return render(request, "main/home.html", context)


@login_required
def meal(request):
    if request.method == "POST":
        dietary = request.POST.get('dietary')
        cuisine = request.POST.get('cuisine')
        meal_type = request.POST.get('meal_type')
        calories = request.POST.get('kcal')
        restriction = request.POST.get('restriction')
        protein_source = request.POST.get('proteinsource')
        cooking_time = request.POST.get('cookingtime')
        budget = request.POST.get('budget')

    data = {
        "header": True,
        "dietary": dietary,
        "cuisine": cuisine,
        "meal_type": meal_type,
        "calories": calories,
        "restriction": restriction,
        "protein_source": protein_source,
        "cooking_time": cooking_time,
        "budget": budget
    }

    response = gemini_api(data)

    meal = json.loads(response)

    context = {
        "title": meal["title"],
        "calories": meal["calories"],
        "description": meal["description"],
        "ingredients": meal["ingredients"],
        "process": meal["process"],
        "duration": meal["duration"],
        "budget": meal["budget"]
    } 

    return render(request, "main/meal.html", context)


@login_required
def history(request):
    context = {
        "header": True,
        "name": "Test"
    }
    return render(request, "main/history.html", context)