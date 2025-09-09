from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('signup/', views.signup_view, name="signup"),
    
    # Features
    path('home/', views.home_view, name="home"),
    path('meal/', views.meal_view, name='meal'),
    path('cook/', views.cook_view, name='cook'),
    path('history/', views.history_view, name="history"),

    # API
    path('meal-api/', views.meal_api, name="meal-api"),
]

