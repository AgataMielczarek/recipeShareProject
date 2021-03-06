from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from .forms import RecForm
from django.contrib.auth.decorators import login_required
from .models import Recipe
from django.db.models import Q

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


        
def detail(request, reId):
    re = get_object_or_404(Recipe, pk=reId)
    return render(request, 'detail.html', {'re':re})

@login_required
def my(request):
    rec = Recipe.objects.filter(user=request.user)
    return render(request, 'my.html', {'rec': rec})


@login_required
def edit(request, reId):
    re = get_object_or_404(Recipe, pk=reId, user=request.user)
    if request.method == 'GET':
        form = RecForm(instance=re)
        return render(request, 'edit.html', {'form': form, 're': re})
    else:
        form = RecForm(request.POST, instance=re)
        if form.is_valid():
            form.save()
            return redirect('my')
        else:
            error = 'Something went wrong. Try again.'
            return render(request, 'edit.html', {'form': form, 're': re, 'error': error})


@login_required
def deleteRec(request, reId):
    re = get_object_or_404(Recipe, pk=reId, user=request.user)
    re.delete()
    return redirect('my')

def search(request):
    keyWords = request.POST.get('search').split(" ")
    for word in keyWords:
        queryset = Recipe.objects.filter(
            Q(name_icontains=word) | Q(ingridiens_icontains=word) | Q(desc_icontains=word))
        try: 
            rec = rec | queryset
        except:
            rec = queryset
    return render(request, 'home.html', {'rec': rec})

def display_cuisine(request, cuisineKey):
    rec = Recipe.objects.filter(cuisine=cuisineKey)
    return render(request, 'home.html', {'rec': rec})

def display_level(request, levelKey):
    rec = Recipe.objects.filter(level=levelKey)
    return render(request, 'home.html', {'rec': rec})    

