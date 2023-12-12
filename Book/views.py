from typing import Any
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.db import models
from django.db.models.query import QuerySet
from django.http import Http404, HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.views.generic.list import ListView
from django.views.generic import DetailView
from django.views.generic import CreateView
from django.views.generic.edit import UpdateView, DeleteView, FormMixin

from Book.models import Recipe, PrivateChoise
from Book.forms import UserRegistrationForm, RecipeForm


class IndexView(TemplateView):
    template_name = 'pages/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Книга рецептов'
        return context


class RecipesListView(ListView):
    model = Recipe
    template_name = 'pages/view_recipes.html'


class UserRecipesListView(LoginRequiredMixin, RecipesListView):
    def get_queryset(self):
        return super().get_queryset().filter(author=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = context['pagename'] = 'Мои рецепты'
        return context


class MainRecipesListView(RecipesListView):
    def get_queryset(self):
        public_recipes = super().get_queryset().filter(private_choise=PrivateChoise.PUBLIC)
        return public_recipes if not self.request.user.is_authenticated else public_recipes | super().get_queryset().filter(author=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = context['pagename'] = 'Все рецепты'
        return context


class RecipeCreateView(LoginRequiredMixin, CreateView):
    form_class = RecipeForm
    template_name = 'pages/add_recipe.html'
    success_url = reverse_lazy('recipes-list')
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class RecipeDetailView(DetailView):
    model = Recipe
    template_name = 'pages/recipe_detail.html'

    def get(self, request, *args, **kwargs):
        recipe = self.get_object()
        if recipe.private_choise == 'PB' or request.user == recipe.author:
            return super().get(request, *args, **kwargs)
        raise Http404


class RecipeUpdateView(LoginRequiredMixin, UpdateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'pages/add_recipe.html'

    def get_success_url(self):
        return reverse_lazy('recipe-detail', args=(self.object.id,))

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.user != kwargs['instance'].author:
            return self.handle_no_permission()
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Редактирование'
        return context


class RecipeDeleteView(LoginRequiredMixin, DeleteView):
    model = Recipe
    template_name = 'pages/recipe_delete.html'
    success_url = reverse_lazy('recipes-list')

    def get(self, request, *args, **kwargs):
        recipe = self.get_object()
        if request.user == recipe.author:
            return super().get(request, *args, **kwargs)
        raise Http404


class UserCreateView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'pages/registration.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Регистрация'
        return context


class UserLoginView(LoginView):
    template_name = 'pages/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['errors'] = 'Неправильное имя или пароль'
        return context


# def logout(request):
#     auth.logout(request)
#     return redirect('home')


# def login(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = auth.authenticate(request, username=username, password=password)
#         if user is not None:
#             auth.login(request, user)
#         else:
#             context = {
#                 'errors': ['Неправильное имя или пароль']
#             }
#             return render(request, 'pages/index.html', context)
#     return redirect('home')
                

# @login_required()
# def my_recipes(request):
#     recipes = Recipe.objects.filter(author=request.user)
#     context = {
#         'pagename': 'Мои рецепты',
#         'recipes': recipes,
#         'count': recipes.count()
#         }
#     return render(request, 'pages/view_recipes.html', context)


# def recipes_page(request):
#     public_recipes = Recipe.objects.filter(private_choise=PrivateChoise.PUBLIC)
#     recipes = public_recipes if not request.user.is_authenticated else public_recipes | Recipe.objects.filter(author=request.user)
#     context = {
#         'pagename': 'Все рецепты',
#         'recipes': recipes,
#         'count': recipes.count()
#         }
#     return render(request, 'pages/view_recipes.html', context)


# @login_required()
# def add_recipe_page(request):
#     if request.method == 'GET':
#         form = RecipeForm()
#         context = {
#             'pagename': 'Добавить рецепт',
#             'form': form
#         }
#         return render(request, 'pages/add_recipe.html', context)    
#     if request.method == 'POST':
#         form = RecipeForm(request.POST, request.FILES)
#         if form.is_valid():
#             recipe = form.save(commit=False)
#             if request.user.is_authenticated:
#                 recipe.author = request.user
#                 recipe.save()
#             return redirect('recipes-list')
#         return render(request,'pages/add_recipe.html', {'form': form})


# def create_user(request):
#     context = {'pagename': 'Регистрация пользователя'}
#     if request.method == 'GET':
#         form = UserRegistrationForm()
#         context['form'] = form
#         return render(request, 'pages/registration.html', context)
#     if request.method == 'POST':
#         form = UserRegistrationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#         context['form'] = form
#         return render(request, 'pages/registration.html', context)

# def recipe_detail(request, recipe_id):
#     recipe = get_object_or_404(Recipe, id=recipe_id)
#     if recipe.private_choise == 'PB' or request.user == recipe.author:
#         return render(request, 'pages/recipe_detail.html', {'recipe': recipe})
#     else:
#         raise Http404

# def recipe_edit(request, recipe_id):
#     recipe = get_object_or_404(Recipe, id=recipe_id)
#     if request.method == 'GET':
#         form = RecipeForm(instance=recipe)
#     if request.method == 'POST':
#         form = RecipeForm(request.POST, request.FILES, instance=recipe)        
#         if form.is_valid():
#             form.save()
#         return redirect('recipe-detail', recipe_id=recipe.id)
#     return render(request, 'pages/add_recipe.html', {'form': form, 'recipe': recipe})

# @login_required()
# def recipe_delete(request, recipe_id):
#     recipe = Recipe.objects.get(id=recipe_id)
#     if request.user == recipe.author:
#         recipe.delete()
#     return redirect('recipes-list')
