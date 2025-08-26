from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
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
def home_view(request):
    return render(request, "main/home.html", {
        "header": True,
    })


@login_required
def meal_view(request):
    if request.method == "POST":
        dietary = request.POST.get('dietary')
        cuisine = request.POST.get('cuisine')
        meal_type = request.POST.get('meal_type')
        calories = request.POST.get('kcal')
        restriction = request.POST.get('restriction')
        protein_source = request.POST.get('proteinsource')
        cooking_time = request.POST.get('cookingtime')
        budget = request.POST.get('budget')

    context = {
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

    meal = gemini_api(context) # test
    data = json.loads(meal) # test

    return render(request, "main/meal.html", data)


@csrf_exempt
def generate_meal(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            request_data = {
                "dietary": data.get('dietary'),
                "cuisine": data.get('cuisine'),
                "meal_type": data.get('meal_type'),
                "calories": data.get('calories'),
                "restriction": data.get('restriction'),
                "protein_source": data.get('protein_source'),
                "cooking_time": data.get('cooking_time'),
                "budget": data.get('budget')  
            }
            print("---request received---")
            
            response = gemini_api(request_data)
            print("---gemini has finally respond---")

            meal = json.loads(response)
            data = {
                "title": meal["title"],
                "calories": meal["calories"],
                "description": meal["description"],
                "ingredients": meal["ingredients"],
                "steps": meal["process"],
                "duration": meal["duration"],
                "budget": meal["budget"]
            }

            return JsonResponse(data)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        
    return JsonResponse({'error': 'Only POST requests allowed'}, status=405)


@login_required
def history_view(request):
    context = {
        "header": True,
        "name": "Test"
    }
    return render(request, "main/history.html", context)