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