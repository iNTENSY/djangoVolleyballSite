from django.core.mail import send_mail
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


from rating.models import Teams


class User(AbstractUser):

    POSITION_TYPES = (
        ('S', 'Связующий'),
        ('MB', 'Центральный блокирующий'),
        ('Li', 'Либеро'),
        ('WS', 'Доигровщик'),
        ('D', 'Диагональный'),
        ('PL', 'Игрок')
    )

    image = models.ImageField('Личное фото', upload_to='user_images', blank=True, null=True)
    team = models.ForeignKey(
        Teams,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Название команды'
    )
    position = models.CharField('Позиция', max_length=25, choices=POSITION_TYPES, default='PL', blank=True)
    is_verified = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class EmailVerification(models.Model):
    code = models.UUIDField(unique=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    expiration = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Пользовательская верификация'
        verbose_name_plural = 'Пользовательские верификации'

    def __str__(self):
        return f'Код верификации для {self.user.username}'

    def send_verification_email(self):
        link = reverse('users:email-verification', kwargs={'email': self.user.email, 'code': self.code})
        verification_link = f'http://127.0.0.1:8000{link}'
        subject = f'Подтверждение учетной записи для {self.user.username}'
        message = 'Для подтверждения учетной записи {} перейдите по ссылке: {}'\
            .format(self.user.username, verification_link)
        send_mail(
            subject=subject,
            message=message,
            from_email='from@example.com',
            recipient_list=[self.user.email],
        )