from typing import Any
from django.contrib.auth.forms import AuthenticationForm
from django.db import models
from django.db.models.query import QuerySet
from django.http import Http404, HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse_lazy, reverse
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.views.generic.list import ListView
from django.views.generic import DetailView
from django.views.generic import CreateView
from django.views.generic.edit import UpdateView, DeleteView, FormMixin

from Book.models import Recipe, PrivateChoise, User, EmailVerification
from Book.forms import UserRegistrationForm, RecipeForm
from common.views import CommonContextMixin


class IndexView(CommonContextMixin, TemplateView):
    template_name = 'pages/index.html'
    title = 'Книга рецептов'


class RecipesListView(ListView):
    model = Recipe
    template_name = 'pages/view_recipes.html'


class UserRecipesListView(LoginRequiredMixin, CommonContextMixin, RecipesListView):
    title = 'Мои рецепты'

    def get_queryset(self):
        return super().get_queryset().filter(author=self.request.user)


class MainRecipesListView(CommonContextMixin, RecipesListView):
    title = 'Все рецепты'

    def get_queryset(self):
        public_recipes = super().get_queryset().filter(private_choise=PrivateChoise.PUBLIC)
        return public_recipes if not self.request.user.is_authenticated else public_recipes | super().get_queryset().filter(author=self.request.user)


class RecipeCreateView(LoginRequiredMixin, CommonContextMixin, CreateView):
    form_class = RecipeForm
    template_name = 'pages/add_recipe.html'
    success_url = reverse_lazy('recipes-list')
    title = 'Добавить рецепт'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class RecipeDetailView(CommonContextMixin, DetailView):
    model = Recipe
    template_name = 'pages/recipe_detail.html'
    title = 'Просмотр рецепта'

    def get(self, request, *args, **kwargs):
        recipe = self.get_object()
        if recipe.private_choise == 'PB' or request.user == recipe.author:
            return super().get(request, *args, **kwargs)
        raise Http404


class RecipeUpdateView(LoginRequiredMixin, CommonContextMixin, UpdateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'pages/add_recipe.html'
    title = 'Редактирование'

    def get_success_url(self):
        return reverse_lazy('recipe-detail', args=(self.object.id,))

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.user != kwargs['instance'].author:
            return self.handle_no_permission()
        return kwargs


class RecipeDeleteView(LoginRequiredMixin, CommonContextMixin, DeleteView):
    model = Recipe
    template_name = 'pages/recipe_delete.html'
    success_url = reverse_lazy('recipes-list')
    title = 'Удаление'

    def get(self, request, *args, **kwargs):
        recipe = self.get_object()
        if request.user == recipe.author:
            return super().get(request, *args, **kwargs)
        raise Http404


class UserCreateView(CommonContextMixin, CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'pages/registration.html'
    success_url = reverse_lazy('home')
    title = 'Регистрация'


class UserLoginView(LoginView):
    template_name = 'pages/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['errors'] = 'Неправильное имя или пароль'
        return context


class EmailVerificationView(CommonContextMixin, TemplateView):
    title = 'Подтверждение электронной почты'
    template_name = 'pages/email_verification.html'

    def get(self, request, *args, **kwargs):
        code = kwargs['code']
        user = User.objects.get(email=kwargs['email'])
        email_verifications = EmailVerification.objects.filter(user=user, code=code)
        if email_verifications.exists() and not email_verifications.first().is_expired():
            user.is_verified_email = True
            user.save()
            return super(EmailVerificationView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('home'))
