from django.urls import path
from . import views
from .views import character_detail, RemoveFromFavoritesView

urlpatterns = [
    path('', views.home, name='home'),
    path('logout/', views.logout_user, name='logout'),
    path('characters_list/', views.characters_list, name='characters_list'),
    path('character/<int:character_id>/', views.character_detail, name='character_detail'),
    path('register/', views.register_user, name='register'),
    path('character/<int:character_id>/post', views.create_post, name='create_post'),
    path('post/<int:post_id>/reply', views.create_reply, name='create_reply'),
    path('character/<int:character_id>/add_to_favorites/', views.add_to_favorites, name='add_to_favorites'),
    path('view_favorites/', views.view_favorites, name='view_favorites'),
    path('characters_list_ajax/', views.characters_list_ajax, name='characters_list_ajax'),
    path('character/<int:character_id>/update_rank/', views.update_rank, name='update_rank'),
    path('character/<int:character_id>/remove_from_favorites/', RemoveFromFavoritesView.as_view(), name='remove_from_favorites'),
    path('character/<int:character_id>/confirm_remove_from_favorites/', views.confirm_remove_from_favorites, name='confirm_remove_from_favorites'),
]