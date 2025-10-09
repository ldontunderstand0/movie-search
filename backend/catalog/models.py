from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.urls import reverse


class User(AbstractUser):

    class Role(models.TextChoices):
        USER = 'Пользователь', 'Пользователь'
        ADMIN = 'Администратор', 'Администратор'
        MODERATOR = 'Модератор', 'Модератор'

    username = models.CharField(max_length=200, verbose_name='Логин', unique=True)
    email = models.EmailField(max_length=200, verbose_name='Почта', unique=True)
    password = models.CharField(max_length=200, verbose_name='Пароль')
    role = models.CharField(max_length=200, verbose_name='Роль', choices=Role.choices, default=Role.USER)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ['username']

    def get_absolute_url(self):
        return reverse('api:profile', args=[self.pk])


class Genre(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название', unique=True)

    objects = models.Manager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"
        ordering = ['name']

    def get_absolute_url(self):
        return reverse('api:genre', args=[self.pk])


class MovieManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(type=Movie.Type.MOVIE)


class SeriesManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(type=Movie.Type.SERIES)


class Movie(models.Model):

    class Type(models.TextChoices):
        MOVIE = 'Фильм', 'Фильм'
        SERIES = 'Сериал', 'Сериал'

    type = models.CharField(max_length=200, verbose_name='Тип', choices=Type.choices, default=Type.MOVIE)
    title = models.CharField(max_length=200, verbose_name='Название')
    release_date = models.DateField(verbose_name='Дата выхода', blank=True, null=True)
    description = models.TextField(verbose_name='Описание', blank=True, null=True)
    rate = models.FloatField(verbose_name='Оценка', blank=True, default=0)
    # rates = models.ManyToManyField('Rate', through='Rating', verbose_name='Оценки', related_name='movies', blank=True)
    genres = models.ManyToManyField('Genre', verbose_name='Жанры', related_name='movies', blank=True)
    countries = models.ManyToManyField('Country', verbose_name='Страны', related_name='movies', blank=True)
    poster = models.ImageField(
        upload_to='images/posters/',  # Папка для загрузки
        blank=True,  # Необязательное поле
        null=True,  # Может быть пустым в БД
        verbose_name='Постер',
        help_text='Загрузите постер фильма'
    )

    objects = models.Manager()
    movies = MovieManager()
    series = SeriesManager()

    def __str__(self):
        return f'{self.title}, {self.release_date}'

    def save(self, *args, **kwargs):
        try:
            old = Movie.objects.get(pk=self.pk)
            if old.poster and old.poster != self.poster:
                old.poster.delete(save=False)
        except Movie.DoesNotExist:
            pass

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.poster:
            self.poster.delete(save=False)
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name = "Кино"
        verbose_name_plural = "Кино"
        ordering = ['-rate']

    def get_absolute_url(self):
        return reverse('api:movie', args=[self.pk])


class Person(models.Model):

    class Type(models.TextChoices):
        MALE = 'Мужчина', 'Мужчина'
        FEMALE = 'Женщина', 'Женщина'

    full_name = models.CharField(max_length=200, verbose_name='ФИО')
    birth_date = models.DateField(verbose_name='Дата рождения', blank=True, null=True)
    sex = models.CharField(max_length=7, verbose_name='Пол', blank=True, null=True, choices=Type.choices)
    biography = models.TextField(verbose_name='Биография', blank=True, null=True)
    movies = models.ManyToManyField(
        'Movie', verbose_name='Фильмы', related_name='movies', through='Profession', blank=True
    )

    def __str__(self):
        return f'{self.full_name}, {self.birth_date}'

    class Meta:
        verbose_name = "Личность"
        verbose_name_plural = "Личности"
        ordering = ['-birth_date']

    def get_absolute_url(self):
        return reverse('api:person', args=[self.pk])


class ActorManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(name=Profession.Type.ACTOR)


class DirectorManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(name=Profession.Type.DIRECTOR)

class Profession(models.Model):

    class Type(models.TextChoices):
        ACTOR = 'актер', 'актер'
        DIRECTOR = 'режиссер', 'режиссер'

    name = models.CharField(max_length=200, verbose_name='Название', choices=Type.choices, default=Type.ACTOR)
    movie = models.ForeignKey('Movie', on_delete=models.PROTECT, verbose_name='Кино', related_name='professions')
    person = models.ForeignKey(
        'Person', on_delete=models.PROTECT, verbose_name='Личность', related_name='professions'
    )

    objects = models.Manager()
    actors = ActorManager()
    directors = DirectorManager()

    def __str__(self):
        return f'person={self.person}, movie={self.movie}, name={self.name}'

    class Meta:
        verbose_name = "Профессия"
        verbose_name_plural = "Профессии"
        ordering = ['name']

    def get_absolute_url(self):
        return reverse('api:profession', args=[self.pk])


class Rating(models.Model):

    class Rate(models.IntegerChoices):
        R1 = 1, '1'
        R2 = 2, '2'
        R3 = 3, '3'
        R4 = 4, '4'
        R5 = 5, '5'
        R6 = 6, '6'
        R7 = 7, '7'
        R8 = 8, '8'
        R9 = 9, '9'
        R10 = 10, '10'

    movie = models.ForeignKey('Movie', on_delete=models.PROTECT, verbose_name='Кино', related_name='ratings')
    user = models.ForeignKey('User', on_delete=models.PROTECT, verbose_name='Пользователь', related_name='ratings')
    rate = models.FloatField(verbose_name='Оценка', choices=Rate.choices, default=Rate.R1)
    date = models.DateTimeField(default=timezone.now, verbose_name='Дата')
    is_watched = models.BooleanField(default=True, verbose_name='Просмотрено')

    objects = models.Manager()

    def __str__(self):
        return f'user={self.user}, movie={self.movie}, rate={self.rate}, date={self.date}'

    class Meta:
        verbose_name = "Оценка"
        verbose_name_plural = "Оценки"
        ordering = ['-date']

    def get_absolute_url(self):
        return reverse('api:rating', args=[self.pk])


class Country(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название', unique=True)

    objects = models.Manager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Страна"
        verbose_name_plural = "Страны"
        ordering = ['name']

    def get_absolute_url(self):
        return reverse('api:country', args=[self.pk])


class Review(models.Model):
    class Type(models.TextChoices):
        POSITIVE = ('Положительная', 'Положительная')
        NEGATIVE = ('Отрицательная', 'Отрицательная')
        NEUTRAL = ('Нейтральная', 'Нейтральная')

    type = models.CharField(max_length=200, verbose_name='Тип', choices=Type.choices)
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')
    movie = models.ForeignKey('Movie', on_delete=models.PROTECT, verbose_name='Кино', related_name='reviews')
    user = models.ForeignKey('User', on_delete=models.PROTECT, verbose_name='Пользователь', related_name='reviews')
    created_at = models.DateTimeField(auto_now_add=timezone.now, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=timezone.now, verbose_name='Дата изменения')

    objects = models.Manager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Рецензия"
        verbose_name_plural = "Рецензии"
        ordering = ['-created_at']

    def get_absolute_url(self):
        return reverse('api:review', args=[self.pk])
