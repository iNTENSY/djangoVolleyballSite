from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Teams(models.Model):
    name = models.CharField('Название команды', max_length=20)
    image = models.ImageField('Символ команды', upload_to='team_images', blank=True, null=True)
    score = models.PositiveSmallIntegerField(
        'Очки команды',
        default=0,
        blank=True,
        validators=[
            MaxValueValidator(1000),
            MinValueValidator(0)
        ],
    )
    players = models.ManyToManyField('users.User', verbose_name='Игроки')

    class Meta:
        verbose_name = 'Команда'
        verbose_name_plural = 'Команды'

    def __str__(self):
        return f'{self.name}'
