from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from marvel_api import get_marvel_characters, get_character_by_id
from django.shortcuts import render, get_object_or_404
from marvel_api import get_marvel_characters, get_character_by_id


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
    characters = get_marvel_characters()
    return render(request, 'characters_list.html', {'characters': characters})

def character_detail(request, character_id):
    character = get_character_by_id(character_id)
    return render(request, 'character_detail.html', {'character': character})
