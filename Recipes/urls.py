from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, include
# from django.views.decorators.cache import cache_page

from Book import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.IndexView.as_view(), name='home'),
    path('recipes/add/', views.RecipeCreateView.as_view(), name='recipes-add'),
    path('recipes/list/', views.MainRecipesListView.as_view(), name='recipes-list'),
    path('recipes/my/', views.UserRecipesListView.as_view(), name='my-recipes'),
    path('recipe/<int:pk>/', views.RecipeDetailView.as_view(), name='recipe-detail'),
    path('recipe/<int:pk>/delete/', views.RecipeDeleteView.as_view(), name='recipe-delete'),
    path('recipe/<int:pk>/edit/', views.RecipeUpdateView.as_view(), name='recipe-edit'),
    path('auth/register/', views.UserCreateView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('verify/<str:email>/<uuid:code>/', views.EmailVerificationView.as_view(), name='email_verification'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


if settings.DEBUG:
    urlpatterns.append(path('__debug__/', include('debug_toolbar.urls')))
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
