from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect

from . import services


# Authentication
def login_view(request):
    return render(request, 'main/login.html')


def logout_view(request):
    pass


def generate_meal_page(request):
    return render(request, "main/generatemealpage.html")


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


def history(request):
    return render(request, "main/history.html")

