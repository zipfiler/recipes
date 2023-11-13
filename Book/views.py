from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.core.exceptions import ObjectDoesNotExist

from Book.models import Recipe, PrivateChoise
from Book.forms import UserRegistrationForm, RecipeForm


def index_page(request):
    return render(request, 'pages/index.html')


@login_required(login_url='login')
def my_recipes(request):
    recipes = Recipe.objects.filter(author=request.user)
    context = {
        'pagename': 'Мои рецепты',
        'recipes': recipes,
        'count': recipes.count()
        }
    return render(request, 'pages/view_recipes.html', context)


@login_required(login_url='login')
def add_recipe_page(request):
    if request.method == 'GET':
        form = RecipeForm()
        context = {
            'pagename': 'Добавить рецепт',
            'form': form
        }
        return render(request, 'pages/add_recipe.html', context)    
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            if request.user.is_authenticated:
                recipe.author = request.user
                recipe.save()
            return redirect('recipes-list')
        return render(request,'pages/add_recipe.html', {'form': form})
        
    
def recipes_page(request):
    recipes = Recipe.objects.filter(private_choise=PrivateChoise.PUBLIC)
    context = {
        'pagename': 'Список рецептов',
        'recipes': recipes,
        'count': recipes.count()
        }
    return render(request, 'pages/view_recipes.html', context)
    

def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if recipe.private_choise == 'PB' or request.user == recipe.author:
        return render(request, 'pages/recipe_detail.html', {'recipe': recipe})
    else:
        raise Http404
     

def recipe_delete(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)
    recipe.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def recipe_edit(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.method == 'GET':
        form = RecipeForm(instance=recipe)
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)        
        if form.is_valid():
            form.save()
        return redirect('recipe-detail', recipe_id=recipe.id)
    return render(request, 'pages/add_recipe.html', {'form': form, 'recipe': recipe})
    

def create_user(request):
    context = {'pagename': 'Регистрация пользователя'}
    if request.method == 'GET':
        form = UserRegistrationForm()
        context['form'] = form
        return render(request, 'pages/registration.html', context)
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        context['form'] = form
        return render(request, 'pages/registration.html', context)


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
        else:
            context = {
                'errors': ['Неправильное имя или пароль']
            }
            return render(request, 'pages/index.html', context)
    return redirect('home')
                

def logout(request):
    auth.logout(request)
    return redirect('home')
