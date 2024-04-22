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
    path('character/<int:character_id>/post', views.create_post, name='create_post'),
    path('post/<int:post_id>/reply', views.create_reply, name='create_reply'),
    path('character/<int:character_id>/add_to_favorites/', views.add_to_favorites, name='add_to_favorites'),
    path('view_favorites/', views.view_favorites, name='view_favorites'),
]