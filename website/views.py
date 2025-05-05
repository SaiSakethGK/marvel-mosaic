from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.models import User

from .forms import SignUpForm
from .models import Post, Reply, FavoriteCharacter
from marvel_api import get_marvel_characters, get_character_by_id

import requests


# ✅ Welcome & Morning Email Support via Zapier Webhook
ZAPIER_WEBHOOK_URL = 'https://hooks.zapier.com/hooks/catch/21605979/2nyzikk/'


from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt  # optional for GET, but safe to add if using external calls
def get_subscribed_users(request):
    if request.method == 'GET':
        users = User.objects.filter(profile__subscribe_news=True)
        data = [
            {
                'email': user.email,
                'name': f"{user.first_name} {user.last_name}"
            }
            for user in users
        ]
        return JsonResponse({'users': data})
    return JsonResponse({'error': 'Invalid request'}, status=400)


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
            messages.error(request, 'Invalid username or password, please try again.')
            return redirect('home')
    return render(request, 'home.html')


def logout_user(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')


def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)

            if form.cleaned_data.get('subscribe_news'):
                user.profile.subscribe_news = True
                user.profile.save()

                # 🔔 Send welcome email if subscribed
                try:
                    requests.post(ZAPIER_WEBHOOK_URL, json={
                        'email': user.email,
                        'name': f"{user.first_name} {user.last_name}",
                        'type': 'welcome'
                    })
                except Exception as e:
                    print("Zapier webhook failed:", e)

            messages.success(request, "You have successfully registered!")
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})


@login_required
def trigger_morning_email(request):
    subscribed_users = User.objects.filter(profile__subscribe_news=True)
    for user in subscribed_users:
        try:
            requests.post(ZAPIER_WEBHOOK_URL, json={
                'email': user.email,
                'name': f"{user.first_name} {user.last_name}",
                'type': 'morning'
            })
        except Exception as e:
            print(f"Zapier webhook failed for {user.email}: {e}")
    return JsonResponse({'status': 'done'})


def subscribed_emails(request):
    if request.method == 'GET':
        emails = list(User.objects.filter(profile__subscribe_news=True).values_list('email', flat=True))
        return JsonResponse({'emails': emails})


@login_required
def characters_list(request):
    search_query = request.GET.get('search', '')
    characters = get_marvel_characters()
    if search_query:
        characters = [c for c in characters if search_query.lower() in c['name'].lower()]

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        characters_html = render_to_string('characters_list_partial.html', {'characters': characters})
        return JsonResponse({'characters_html': characters_html})
    return render(request, 'characters_list.html', {'characters': characters})


def character_detail(request, character_id):
    character = get_character_by_id(character_id)
    posts = Post.objects.filter(character_id=character_id).order_by('-created_at')
    return render(request, 'character_detail.html', {'character': character, 'posts': posts})


@login_required
def add_to_favorites(request, character_id):
    user = request.user
    if not FavoriteCharacter.objects.filter(user=user, character_id=character_id).exists():
        FavoriteCharacter.objects.create(user=user, character_id=character_id)
        messages.success(request, "Character added to favorites!")
    else:
        messages.info(request, "Character already in favorites!")
    return redirect('character_detail', character_id=character_id)


@login_required
def view_favorites(request):
    user = request.user
    favorite_characters = FavoriteCharacter.objects.filter(user=user).order_by('rank')
    characters_data = []

    for fc in favorite_characters:
        character = get_character_by_id(fc.character_id)
        if character:
            characters_data.append({
                'id': fc.character_id,
                'name': character['name'],
                'image_url': f"{character['thumbnail']['path']}.{character['thumbnail']['extension']}",
                'rank': fc.rank
            })

    return render(request, 'favorites.html', {
        'characters_data': characters_data,
        'no_characters_found': not characters_data,
        'range': list(range(1, len(favorite_characters) + 1))
    })


@login_required
def update_rank(request, character_id):
    favorite_character = get_object_or_404(FavoriteCharacter, user=request.user, character_id=character_id)
    if request.method == 'POST':
        new_rank = request.POST.get('rank')
        favorite_character.rank = new_rank
        favorite_character.save()
    return redirect('view_favorites')


def confirm_remove_from_favorites(request, character_id):
    character = get_character_by_id(character_id)
    return render(request, 'confirm_remove.html', {'character': character})


@method_decorator(login_required, name='dispatch')
class RemoveFromFavoritesView(View):
    def post(self, request, character_id):
        favorite_character = FavoriteCharacter.objects.filter(user=request.user, character_id=character_id).first()
        if favorite_character:
            character = get_character_by_id(character_id)
            messages.success(request, f"{character['name']} removed from favorites!")
            favorite_character.delete()
        else:
            messages.info(request, "Character not in favorites!")
        return redirect('view_favorites')


@login_required
def create_post(request, character_id):
    if request.method == 'POST':
        Post.objects.create(user=request.user, character_id=character_id, content=request.POST['content'])
    return redirect('character_detail', character_id=character_id)


@login_required
def create_reply(request, post_id):
    if request.method == 'POST':
        post = Post.objects.get(id=post_id)
        Reply.objects.create(user=request.user, post=post, content=request.POST['content'])
    return redirect('character_detail', character_id=post.character_id)
