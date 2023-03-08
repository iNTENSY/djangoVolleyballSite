from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import User


class Category(models.Model):
    rank = models.CharField('Звание', max_length=20, unique=True)

    class Meta:
        verbose_name = 'Умение'
        verbose_name_plural = 'Умения'

    def __str__(self):
        return self.rank


class Post(models.Model):
    date_time_start = models.DateTimeField('Дата начала мероприятия')
    date_time_end = models.DateTimeField('Дата окончания мероприятия')
    description = models.TextField(
        verbose_name='Доп. информация',
        default='Волейбол, «Муссон». Игроков: мин.12/мах.18.Стоимость: ~100 - 150 руб. '
                '⚠У кого есть мяч 🏐, просьба взять с собой. ❗Записался и не пришёл? Бан на неделю',
        null=True,
        blank=True
    )
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, verbose_name='Категория', null=True)
    reservation = models.PositiveSmallIntegerField(
        'Количество свободных мест',
        default=18,
        validators=[MaxValueValidator(18), MinValueValidator(0)],
        blank=True
    )
    on_main = models.BooleanField('Опубликовать на главную страницу?', default=False)

    class Meta:
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'

    def __str__(self):
        return f'[{self.category}] {self.date_time_start.strftime("%d.%m.%Y %H:%M")} - ' \
               f'{self.date_time_end.strftime("%d.%m.%Y %H:%M")}'


class Reservations(models.Model):
    title = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True, verbose_name='Название публикации')
    players = models.ManyToManyField(User, verbose_name='Имя пользователя')
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Регистрация на игру'
        verbose_name_plural = 'Регистрации на игру'

    def __str__(self):
        return f'Регистрация на: {self.title.date_time_start.strftime("%d.%m.%Y %H:%M")}'
