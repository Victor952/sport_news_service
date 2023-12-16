from django.db import models
from sport_news.utils import from_cyrillic_to_eng
class City(models.Model):
    name = models.CharField(max_length=50, unique=True,  # name - поле
                            verbose_name='Название населённого пункта')
    slug = models.CharField(max_length=50, unique=True, blank=True)
    class Meta:
        verbose_name = 'Название населённого пункта'
        verbose_name_plural = 'Названия населённых пунктов'
    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = from_cyrillic_to_eng(str(self.name))
        super().save(*args, **kwargs)
class Sport_type(models.Model):
    name = models.CharField(max_length=50, unique=True,
                            verbose_name='Вид спорта')
    slug = models.CharField(max_length=50, unique=True, blank=True)
    class Meta:
        verbose_name = 'Вид спорта'
        verbose_name_plural = 'Виды спорта'
    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = from_cyrillic_to_eng(str(self.name))
        super().save(*args, **kwargs)
class News(models.Model):
    url = models.URLField(unique=True)
    title = models.CharField(max_length=250, verbose_name='Заголовок новости')
    description = models.TextField(verbose_name='Описание')
    city = models.ForeignKey('City', on_delete=models.CASCADE,
                             verbose_name='Город')
    sport_type = models.ForeignKey('Sport_type', on_delete=models.CASCADE, verbose_name='Вид спорта')
    timestamp = models.DateField(auto_now_add=True)
    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
    def __str__(self):
        return self.title