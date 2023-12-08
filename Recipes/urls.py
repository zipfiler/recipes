from django.contrib import admin
from django.urls import path

from Book import views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.IndexView.as_view(), name='home'),
    path('recipes/add', views.RecipeCreateView.as_view(), name='recipes-add'),
    path('recipes/list', views.MainRecipesListView.as_view(), name='recipes-list'),
    path('recipes/my', views.UserRecipesListView.as_view(), name='my-recipes'),
    path('recipe/<int:recipe_id>', views.recipe_detail, name='recipe-detail'),
    path('recipe/<int:recipe_id>/delete', views.recipe_delete, name='recipe-delete'),
    path('recipe/<int:pk>/edit', views.RecipeUpdateView.as_view(), name='recipe-edit'),
    # path('recipe/<int:recipe_id>/edit', views.recipe_edit, name='recipe-edit'),
    path('auth/register', views.UserCreateView.as_view(), name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)