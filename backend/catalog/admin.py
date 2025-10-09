from django.contrib import admin
from . import models


class ProfessionInline(admin.StackedInline):
    model = models.Profession
    extra = 0
    can_delete = False
    verbose_name = 'Профессия'
    verbose_name_plural = 'Профессия'
    fields = ['name', 'movie', 'person']


class RatingInline(admin.StackedInline):
    model = models.Rating
    extra = 0
    can_delete = False
    verbose_name = 'Оценка'
    verbose_name_plural = 'Оценка'
    fields = ['rate', 'date', 'movie', 'user']


class ReviewInline(admin.StackedInline):
    model = models.Review
    extra = 0
    can_delete = False
    verbose_name = 'Рецензия'
    verbose_name_plural = 'Рецензия'
    fields = ['title', 'text', 'date', 'movie', 'user']


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'password_display', 'role']
    list_filter = ['role']
    inlines = [RatingInline, ReviewInline]
    list_display_links = ['username']
    search_fields = ['username', 'email']
    readonly_fields = ['password_display']

    @admin.display()
    def password_display(self, obj):
        return "••••••••"
    password_display.short_description = 'Пароль (зашифрован)'


@admin.register(models.Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = [
        'type',
        'title',
        'release_date',
        'description_display',
        'display_genres',
        'display_countries',
        'poster'
    ]
    list_filter = ['type', 'genres']
    inlines = [ProfessionInline, RatingInline, ReviewInline]
    date_hierarchy = 'release_date'
    filter_horizontal = ('genres', 'countries')
    list_display_links = ['title']
    search_fields = ['title', 'description']

    @admin.display()
    def description_display(self, obj):
        return obj.description[:30] + '...' if len(obj.description) > 30 else obj

    description_display.short_description = 'Описание'

    @admin.display()
    def display_genres(self, obj):
        return ", ".join([genre.name for genre in obj.genres.all()])
    display_genres.short_description = 'Жанры'

    @admin.display()
    def display_countries(self, obj):
        return ", ".join([country.name for country in obj.countries.all()])

    def poster_preview(self, obj):
        if obj.poster:
            return f'<img src="{obj.poster.url}" style="max-height: 100px;" />'
        return "Нет постера"
    poster_preview.allow_tags = True
    poster_preview.short_description = 'Превью постера'

    display_countries.short_description = 'Страны'


@admin.register(models.Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'birth_date', 'sex', 'biography_display', 'display_movies']
    list_filter = ['sex']
    inlines = [ProfessionInline]
    date_hierarchy = 'birth_date'
    list_display_links = ['full_name']
    search_fields = ['full_name']

    @admin.display()
    def biography_display(self, obj):
        return obj.biography[:30] + '...' if len(obj.biography) > 30 else obj
    biography_display.short_description = 'Биография'

    @admin.display()
    def display_movies(self, obj):
        return ", ".join([movie.title for movie in obj.movies.all()])

    display_movies.short_description = 'Фильмы'


@admin.register(models.Profession)
class ProfessionAdmin(admin.ModelAdmin):
    list_display = ['name', 'movie', 'person']
    list_filter = ['name', 'movie', 'person']
    list_display_links = ['name']
    raw_id_fields = ['movie', 'person']
    search_fields = ['name']


@admin.register(models.Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['rate', 'date', 'movie', 'user']
    list_filter = ['rate', 'date', 'movie', 'user']
    date_hierarchy = 'date'
    list_display_links = ['rate']
    raw_id_fields = ['movie', 'user']


@admin.register(models.Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_display_links = ['name']
    search_fields = ['name']


@admin.register(models.Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_display_links = ['name']
    search_fields = ['name']


@admin.register(models.Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['title', 'text', 'movie', 'user', 'created_at', 'updated_at']
    list_filter = ['movie', 'user']
    date_hierarchy = 'created_at'
    list_display_links = ['title']
    raw_id_fields = ['movie', 'user']
