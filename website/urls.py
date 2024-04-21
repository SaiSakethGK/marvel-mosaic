from django.urls import path
from . import views
from .views import character_detail
# Import the missing attribute if necessary
urlpatterns = [
    path('', views.home, name='home'),
    # path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('characters_list/', views.characters_list, name='characters_list'),
    path('character/<int:character_id>/', views.character_detail, name='character_detail'),
    path('register/', views.register_user, name='register'),
]