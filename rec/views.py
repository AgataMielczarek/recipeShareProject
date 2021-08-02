from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from .forms import RecForm
from django.contrib.auth.decorators import login_required
from .models import Recipe

def register(request):
    if request.method == 'GET':
        return render(request, 'register.html', {'form': UserCreationForm()})
    else:
        if request.POST.get('password1') == request.POST.get('password2'):
            try:
                user = User.objects.create_user(username=request.POST.get(
                    'username'), passwoer=request.POST.get('password2'))
            except IntegrityError:
                error = 'This username is already taken. Try another one.'
                return render(request, 'register.html', {'form':UserCreationForm(), 'error': error})
            else:
                user.save()
                login(request, user)
                return redirect('home')
        else:
            error = 'Password did not match. Try again.'
            return render(request, 'register.html', {'form': UserCreationForm, 'error': error})

def log(request):
    if request.method == 'GET':
        return render(request, 'log.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(username=request.POST.get(
            'username'), password=request.POST.get('password'))
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            error = 'Username or password is wrong. Try again.'
            return render(request, 'log.html', {'form': AuthenticationForm(), 'error': error})

@login_required
def logoutuser(request):
    logout(request)
    return redirect('home')


def home(request):
    rec = Recipe.objects.all()
    return render(request, 'home.html', {'rec': rec})

@login_required
def create(request):
    if request.method == 'GET':
        return render(request, 'create.html', {'form': RecForm()})
    else:
        form = RecForm(request.POST)
        if form.is_valid():
            re = form.save(commit=False)
            re.user = request.user 
            re.save()
            return redirect ('home')
        else:
            error = 'Something went wrong. Try again.'
            return render(request, 'create.html', {'form': RecForm(), 'error': error})

        


