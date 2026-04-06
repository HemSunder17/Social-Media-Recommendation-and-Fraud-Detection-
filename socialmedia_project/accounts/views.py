from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User, Interest, INTEREST_CHOICES


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, 'Passwords do not match')
            return redirect('accounts:register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken')
            return redirect('accounts:register')

        user = User.objects.create_user(username=username, email=email, password=password1)
        login(request, user)
        return redirect('accounts:interests')

    return render(request, 'accounts/register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('posts:feed')
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    return redirect('accounts:login')


@login_required
def select_interests(request):
    if request.method == 'POST':
        selected = request.POST.getlist('interests')
        request.user.interests.clear()
        for name in selected:
            interest, _ = Interest.objects.get_or_create(name=name)
            request.user.interests.add(interest)
        return redirect('posts:feed')

    user_interest_names = list(request.user.interests.values_list('name', flat=True))
    return render(request, 'accounts/interests.html', {
        'interests': INTEREST_CHOICES,
        'user_interest_names': user_interest_names,
    })


@login_required
def profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    user_posts = profile_user.posts.filter(is_flagged=False).order_by('-created_at')
    return render(request, 'accounts/profile.html', {
        'profile_user': profile_user,
        'user_posts': user_posts,
    })