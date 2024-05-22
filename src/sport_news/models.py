import jsonfield
from django.db import models
from .utils import from_cyrillic_to_eng
def default_urls():
    return {"sport24": "", "sovsport": "", "sportuspro": "", "bezfromata": ""}
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
class Stype(models.Model):
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
class Newsc(models.Model):
    objects = None
    url = models.URLField(unique=True)
    title = models.CharField(max_length=250, verbose_name='Заголовок новости')
    description = models.TextField(verbose_name='Описание')
    city = models.ForeignKey('City', on_delete=models.CASCADE, verbose_name='Город')
    timestamp = models.DateField(auto_now_add=True)
    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости по городу'
        ordering = ['-timestamp']  # данные в обратном порядке идут сверху вниз
    def __str__(self):
        return self.title
class Newsst(models.Model):
    objects = None
    url = models.URLField(unique=True)
    title = models.CharField(max_length=250, verbose_name='Заголовок новости')
    description = models.TextField(verbose_name='Описание')
    stype = models.ForeignKey('Stype', on_delete=models.CASCADE, verbose_name='Вид спорта')
    timestamp = models.DateField(auto_now_add=True)
    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости по виду спорта'
        ordering = ['-timestamp']  # данные в обратном порядке идут сверху вниз
    def __str__(self):
        return self.title
class Error(models.Model):
    objects = None
    timestamp = models.DateField(auto_now_add=True)
    data = jsonfield.JSONField()
    def __str__(self):
        return str(self.timestamp)
class Url(models.Model):
    objects = None
    url_data = jsonfield.JSONField(default=default_urls)