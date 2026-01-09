from django.db import models
from django.contrib.auth.models import User


class Genre(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название жанра')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class RecordCondition(models.Model):
    CONDITION_CHOICES = [
        ('M', 'Mint'),
        ('VG', 'Very good'),
        ('G', 'Good'),
        ('F', 'Fair'),
    ]

    grade = models.CharField(max_length=4, choices=CONDITION_CHOICES, verbose_name='Состояние')
    description = models.TextField(verbose_name='Описание', blank=True)

    def __str__(self):
        return f'{self.get_grade_display()} ({self.description})'

    class Meta:
        verbose_name = "Состояние пластинки"
        verbose_name_plural = "Состояния пластинок"
        ordering = ['grade']


class VinylRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Владелец')
    title = models.CharField(max_length=200, verbose_name='Название альбома')
    artist = models.CharField(max_length=200, verbose_name='Исполнитель')
    year = models.IntegerField(verbose_name='Год выпуска')
    estimated_value = models.DecimalField(max_digits=10, decimal_places=2,
                                          verbose_name='Оценочная стоимость', default=0.00)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2,
                                         verbose_name='Цена покупки', null=True, blank=True)

    FORMAT_CHOICES = [
        ('LP', 'LP (альбом)'),
        ('EP', 'EP (мини-альбом)'),
        ('S', 'Сингл'),
        ('BOX', 'Бокс-сет'),
    ]

    format = models.CharField(max_length=4, choices=FORMAT_CHOICES, default='LP', verbose_name='Формат')
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL,
                              null=True, blank=True, verbose_name='Жанр')
    condition = models.ForeignKey(RecordCondition, on_delete=models.SET_NULL,
                                  null=True, blank=True, verbose_name='Состояние')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    update_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    def __str__(self):
        return f'{self.artist} - {self.title} ({self.year})'

    class Meta:
        verbose_name = "Виниловая пластинка"
        verbose_name_plural = "Виниловые пластинки"
        ordering = ['artist', 'year']
