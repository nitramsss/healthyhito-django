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
    path('history/', views.history_view, name="history"),
    path('meal-api/', views.generate_meal, name="meal-api")
]

