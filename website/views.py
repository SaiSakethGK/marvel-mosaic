from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from marvel_api import get_marvel_characters, get_character_by_id
from django.shortcuts import render, get_object_or_404
from marvel_api import get_marvel_characters, get_character_by_id
from .forms import SignUpForm
from django.contrib.auth.decorators import login_required
from .models import Post
from django.contrib.auth.decorators import login_required
from .models import Post, Reply
from .models import FavoriteCharacter
from django.http import JsonResponse
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


@method_decorator(login_required, name='dispatch')
class RemoveFromFavoritesView(View):
    def post(self, request, character_id):
        user = request.user
        # Check if the character is in favorites
        favorite_character = FavoriteCharacter.objects.filter(user=user, character_id=character_id).first()
        if favorite_character:
            character = get_character_by_id(character_id)
            character_name = character['name']
            favorite_character.delete()
            messages.success(request, f"{character_name} removed from favorites!")
        else:
            messages.info(request, "Character not in favorites!")
        return redirect('view_favorites')
    

def characters_list_ajax(request):
    search_query = request.GET.get('search', '')
    if search_query:
        characters = [character for character in get_marvel_characters() if search_query.lower() in character['name'].lower()]
    else:
        characters = get_marvel_characters()
    return render(request, 'characters_list.html', {'characters': characters})

@login_required
def add_to_favorites(request, character_id):
    user = request.user
    # Check if the character is already in favorites
    if not FavoriteCharacter.objects.filter(user=user, character_id=character_id).exists():
        FavoriteCharacter.objects.create(user=user, character_id=character_id)
        messages.success(request, "Character added to favorites!")
    else:
        messages.info(request, "Character already in favorites!")
    return redirect('character_detail', character_id=character_id)

@login_required
def view_favorites(request):
    user = request.user
    favorite_characters = FavoriteCharacter.objects.filter(user=user)
    characters_data = []
    for favorite_character in favorite_characters:
        character_id = favorite_character.character_id
        character = get_character_by_id(character_id)
        characters_data.append({
            'id': character_id,
            'name': character['name'],
            'image_url': f"{character['thumbnail']['path']}.{character['thumbnail']['extension']}"
        })

    no_characters_found = len(characters_data) == 0

    return render(request, 'favorites.html', {'characters_data': characters_data, 'no_characters_found': no_characters_found})


def home(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back {username}')
            return redirect('home')
        else:
            messages.success(request, 'Invalid username or password, Please try again...')
            return redirect('home')


    else:
        return render(request, 'home.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, 'You have been logged out...')
    return redirect('home')


def characters_list(request):
    search_query = request.GET.get('search', '')
    if search_query:
        characters = [character for character in get_marvel_characters() if search_query.lower() in character['name'].lower()]
    else:
        characters = get_marvel_characters()
    return render(request, 'characters_list.html', {'characters': characters})


def character_detail(request, character_id):
    character = get_character_by_id(character_id)
    posts = Post.objects.filter(character_id=character_id).order_by('-created_at')
    return render(request, 'character_detail.html', {'character': character, 'posts': posts})

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # Authenticate and login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You Have Successfully Registered! Welcome!")
            return redirect('home')
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form': form})

    return render(request, 'register.html', {'form': form})

@login_required
def create_post(request, character_id):
    if request.method == 'POST':
        content = request.POST['content']
        Post.objects.create(user=request.user, character_id=character_id, content=content)
        return redirect('character_detail', character_id=character_id)


@login_required
def create_reply(request, post_id):
    if request.method == 'POST':
        content = request.POST['content']
        post = Post.objects.get(id=post_id)
        Reply.objects.create(user=request.user, post=post, content=content)
        return redirect('character_detail', character_id=post.character_id)
    