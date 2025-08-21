from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('signup/', views.signup_view, name="signup"),
    
    # Features
    path('home/', views.home, name="home"),
    path('meal/', views.show_meal, name='meal'),
    path('history/', views.history, name="history"),
]

