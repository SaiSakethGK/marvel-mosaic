from django.urls import path
from . import views

# Check if 'views.py' contains a 'home' function
# If it does, import it and use it as the second argument in the 'path' function
# If it doesn't, create the 'home' function in 'views.py'

urlpatterns = [
    path('', views.home, name='home'),
    # path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
]