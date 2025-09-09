from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
from .models import User, UserProfile, UserHistory
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
        password= request.POST.get("password")
        confirm_password= request.POST.get("confirm_password")

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

        return render(request, "main/meal.html", context)

    return render(request, "main/error.html", {
        "header": True
    })


@csrf_exempt
def meal_api(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            user_data = {
                "dietary": data.get('dietary'),
                "cuisine": data.get('cuisine'),
                "meal_type": data.get('meal_type'),
                "calories": data.get('kcal'),
                "restriction": data.get('restriction'),
                "protein_source": data.get('proteinsource'),
                "cooking_time": data.get('cookingtime'),
                "budget": data.get('budget'),
            }
            
            gemini_response = gemini_api(user_data) 
            meal_data = json.loads(gemini_response)
            processed_data = {
                "title": meal_data["title"],
                "calories": meal_data["calories"],
                "description": meal_data["description"],
                "ingredients": meal_data["ingredients"],
                "steps": meal_data["process"],
                "duration": meal_data["duration"],
                "budget": meal_data["budget"],
            }
            print(processed_data)
            return JsonResponse(processed_data)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    return JsonResponse({"error": "Only POST requests allowed"}, status=405)


@login_required
def cook_view(request):
    if request.method == "POST":
        json_data = request.POST.get('meal_data')
        meal_data = json.loads(json_data)
        
        # Get data individually
        title = meal_data.get('title')
        calories = float(meal_data.get('calories'))
        description = meal_data.get('description')
        ingredients = str(meal_data.get('recipes'))
        steps = str(meal_data.get('steps'))
        duration = meal_data.get('duration')
        budget = meal_data.get('budget')

        # Save data
        user_history = UserHistory.objects.create(
            user=request.user,
            title=title,
            calories=calories,
            description=description,
            ingredients=ingredients,
            steps=steps,
            duration=duration,
            budget=budget,
        )
        print(user_history)
        user_history.save()
        print("***Data Saved***")
        
        return HttpResponseRedirect(reverse('home'))

    return render(request, 'main/cook.html', {
        'header': True
    })


@login_required
def history_view(request):
    user_history_data = UserHistory.objects.filter(user=request.user)
    context = {
        "header": True,
        "data": user_history_data,
    }
    return render(request, "main/history.html", context)