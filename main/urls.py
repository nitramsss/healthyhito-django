from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    
    path('', views.generate_meal_page, name="generate_meal"),
    path('meal/', views.show_meal, name='show_meal'),
    path('history/', views.history, name="history"),
]

