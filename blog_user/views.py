from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import LoginForm


def login_user(request):
    context = {
        'form': LoginForm()
    }
    if request.method == "POST":
        form = LoginForm(request.POST)
        username = form.data.get('username')
        password = form.data.get('password')
        if username and password:
            user = authenticate(
                request, username=username,
                password=password
            )
            print(user)
            if user is not None:
                login(request, user)
                messages.add_message(
                    request, messages.SUCCESS, 
                    f'Welcome {username}'
                )
                return redirect('home')
            else:
                messages.add_message(
                    request, messages.WARNING, 
                    'You could not sign in'
                )
    return render(request, 'blog_user/login.html', context)


def logout_user(request):
    logout(request)
    messages.add_message(
        request, messages.SUCCESS, 
        'You sign out'
    )
    return redirect('home')


def sign_up(request):
    if request.method == "POST":
        r_post = request.POST
        username = r_post.get('email')
        password = r_post.get('password')
        password2 = r_post.get('password2')
        if username and (password == password2):
            user, created = User.objects.get_or_create(
                username=username, 
                email=username
            )
            if created:
                user.set_password(password)
                user.save()
            auth = authenticate(
                request, username=username,
                password=password
            )
            login(request, auth)
            return redirect('home')

    return render(request, 'blog_user/sign_up.html',{})
