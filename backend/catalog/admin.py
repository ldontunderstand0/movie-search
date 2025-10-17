from django.contrib import admin, messages
from django.urls import reverse
from django.utils.safestring import mark_safe
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
    fields = ['rate', 'movie', 'user']


class ReviewInline(admin.StackedInline):
    model = models.Review
    extra = 0
    can_delete = False
    verbose_name = 'Рецензия'
    verbose_name_plural = 'Рецензия'
    fields = ['title', 'text', 'movie', 'user', 'status']


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'password_display', 'role']
    list_filter = ['role']
    inlines = [RatingInline, ReviewInline]
    list_display_links = ['username']
    search_fields = ['username', 'email']

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
        'poster_preview',
        'trailer_url'
    ]
    list_filter = ['type', 'genres']
    inlines = [ProfessionInline, RatingInline, ReviewInline]
    date_hierarchy = 'release_date'
    filter_horizontal = ('genres', 'countries')
    list_display_links = ['title']
    search_fields = ['title', 'description']
    readonly_fields = ('poster_detail_preview',)

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

    @admin.display()
    def poster_preview(self, obj):
        if obj.poster:
            return mark_safe(f'<img src="{obj.poster.url}" width="40" />')
        return "Нет постера"
    poster_preview.allow_tags = True
    poster_preview.short_description = 'Превью постера'

    def poster_detail_preview(self, obj):
        if obj.poster:
            return mark_safe(f'<img src="{obj.poster.url}" width="200" />')
        return "Нет постера"
    poster_detail_preview.allow_tags = True
    poster_detail_preview.short_description = 'Текущий постер'

    display_countries.short_description = 'Страны'


@admin.register(models.Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'birth_date', 'sex', 'display_biography', 'display_movies']
    list_filter = ['sex']
    inlines = [ProfessionInline]
    date_hierarchy = 'birth_date'
    list_display_links = ['full_name']
    search_fields = ['full_name']

    @admin.display()
    def display_movies(self, obj):
        return ", ".join([movie.title for movie in obj.movies.all()[:5]])

    display_movies.short_description = 'Фильмы'

    @admin.display()
    def display_biography(self, obj):
        if obj.biography and obj.biography.path.endswith(('.txt', '.srt')):
            try:
                with open(obj.biography.path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Ограничим длину, чтобы не раздувать таблицу
                    if len(content) > 100:
                        content = content[:100] + "…"
                    # Для админки лучше оставить переносы как есть
                    return content
            except Exception as e:
                return f"Ошибка: {e}"
        return "Нет биографии"

    display_biography.short_description = 'Биография'




@admin.register(models.Profession)
class ProfessionAdmin(admin.ModelAdmin):
    list_display = ['name', 'movie', 'person']
    list_filter = ['name', 'movie', 'person']
    list_display_links = ['name']
    raw_id_fields = ['movie', 'person']
    search_fields = ['name']


@admin.register(models.Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['rate', 'movie', 'user', 'created_at', 'updated_at']
    list_filter = ['rate', 'movie', 'user']
    date_hierarchy = 'created_at'
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
    list_display = ['title', 'text_display', 'movie', 'user', 'created_at', 'updated_at', 'status', 'review_pdf']
    list_filter = ['status', 'movie', 'user']
    date_hierarchy = 'created_at'
    list_display_links = ['title']
    raw_id_fields = ['movie', 'user']
    actions = ['approve_reviews', 'reject_reviews']

    @admin.display()
    def text_display(self, obj):
        return obj.text[:30] + '...' if len(obj.text) > 30 else obj
    text_display.short_description = 'Текст'

    @admin.display()
    def review_pdf(self, obj):
        url = reverse('catalog:admin_review_pdf', args=[obj.id])
        return mark_safe(f'<a href="{url}">PDF</a>')

    def approve_reviews(self, request, queryset):
        updated = queryset.update(status=models.Review.Status.APPROVED)
        self.message_user(request, f'{updated} рецензий одобрено', messages.SUCCESS)
    approve_reviews.short_description = "Одобрить выбранные рецензии"
    
    def reject_reviews(self, request, queryset):
        updated = queryset.update(status=models.Review.Status.NOT_APPROVED)
        self.message_user(request, f'{updated} рецензий отклонено', messages.SUCCESS)
    reject_reviews.short_description = "Отклонить выбранные рецензии"

    review_pdf.short_description = 'PDF со статусом'
