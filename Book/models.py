from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.timezone import now


class User(AbstractUser):
    is_verified_email = models.BooleanField(default=False)
    email = models.EmailField(unique=True, blank=False)


TYPES = (
    ('Первое', 'первое'),
    ('Второе', 'второе'),
    ('Салат', 'салат'),
    ('Десерт', 'десерт'),
    ('Прочее', 'прочее'),
)


class PrivateChoise(models.TextChoices):
    PRIVATE = 'PR', 'Сохранить черновик (виден мне)'
    PUBLIC = 'PB', 'Добавить рецепт (виден всем)'


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


class EmailVerification(models.Model):
    code = models.UUIDField(unique=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField()

    def __str__(self):
        return f'EmailVerification object for {self.user.email}'

    def send_verification_email(self):
        link = reverse('email_verification', kwargs={'email': self.user.email, 'code': self.code})
        verification_link = f'{settings.DOMAIN_NAME}{link}'
        subject = f'Подтверждение учётной записи для {self.user.username}'
        message = 'Для подтверждения учётной записи для {} перейдите по ссылке: {}'.format(
            self.user.email,
            verification_link
        )
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.user.email],
            fail_silently=False,
        )

    def is_expired(self):
        return now() >= self.expiration
