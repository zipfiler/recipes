from django.db import models
from django.contrib.auth.models import User


TYPES = (
    ('Первое', 'первое'),
    ('Второе', 'второе'),
    ('Салат', 'салат'),
    ('Десерт', 'десерт'),
    ('Прочее', 'прочее'),
)


class PrivateChoise(models.TextChoices):
    PRIVATE = 'PR', 'Загрузить приватно'
    PUBLIC = 'PB', 'Добавить в Книгу рецептов'


class Recipe(models.Model):
    class Meta:
        ordering = ['-published_date']

    author = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=200)
    text = models.TextField(max_length=5000)
    image = models.ImageField(upload_to='recipes_images', blank=True)
    type = models.CharField(max_length=30, choices=TYPES, blank=True)
    published_date = models.DateTimeField(auto_now=True)
    private_choise = models.CharField(
        max_length=2,
        choices=PrivateChoise.choices,
        default=PrivateChoise.PUBLIC,
    )
    
    def __str__(self):
        return f'{self.title}. Автор: {self.author}'
    
    
