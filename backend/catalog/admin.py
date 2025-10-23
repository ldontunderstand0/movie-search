from django.contrib import admin, messages
from django.urls import reverse
from django.utils.safestring import mark_safe
from catalog import models


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
        if obj.description:
            return obj.description[:30] + '...' if len(obj.description) > 30 else obj
        return ''

    @admin.display()
    def display_genres(self, obj):
        return ", ".join(obj.genres.values_list('name', flat=True))

    @admin.display()
    def display_countries(self, obj):
        return ", ".join(obj.countries.values_list('name', flat=True))

    @admin.display()
    def poster_preview(self, obj):
        return mark_safe(f'<img src="{obj.poster.url}" width="40" />') if obj.poster else 'Нет постера'

    @admin.display()
    def poster_detail_preview(self, obj):
        return mark_safe(f'<img src="{obj.poster.url}" width="200" />') if obj.poster else "Нет постера"

    description_display.short_description = 'Описание'
    display_genres.short_description = 'Жанры'
    display_countries.short_description = 'Страны'
    poster_preview.allow_tags = True
    poster_preview.short_description = 'Превью постера'
    poster_detail_preview.allow_tags = True
    poster_detail_preview.short_description = 'Текущий постер'


@admin.register(models.Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'birth_date', 'sex', 'display_biography', 'display_movies', 'photo_preview']
    list_filter = ['sex']
    inlines = [ProfessionInline]
    date_hierarchy = 'birth_date'
    list_display_links = ['full_name']
    search_fields = ['full_name']
    readonly_fields = ('photo_detail_preview',)

    @admin.display()
    def display_movies(self, obj):
        return ", ".join(obj.movies.values_list('title', flat=True)[:5])

    @admin.display()
    def display_biography(self, obj):
        if obj.biography and obj.biography.path.endswith(('.txt', '.srt')):
            with open(obj.biography.path, 'r', encoding='utf-8') as f:
                content = f.read()
                return content[:100] + "…" if len(content) > 100 else content
        return "Нет биографии"

    @admin.display()
    def photo_preview(self, obj):
        return mark_safe(f'<img src="{obj.photo.url}" width="40" />') if obj.photo else 'Нет фото'

    @admin.display()
    def photo_detail_preview(self, obj):
        return mark_safe(f'<img src="{obj.photo.url}" width="200" />') if obj.photo else "Нет фото"

    display_movies.short_description = 'Фильмы'
    display_biography.short_description = 'Биография'
    photo_preview.allow_tags = True
    photo_preview.short_description = 'Превью фото'
    photo_detail_preview.allow_tags = True
    photo_detail_preview.short_description = 'Текущее фото'


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

    @admin.display()
    def review_pdf(self, obj):
        url = reverse('catalog:admin_review_pdf', args=[obj.id])
        return mark_safe(f'<a href="{url}">PDF</a>')

    def approve_reviews(self, request, queryset):
        updated = queryset.update(status=models.Review.Status.APPROVED)
        self.message_user(request, f'{updated} рецензий одобрено', messages.SUCCESS)

    def reject_reviews(self, request, queryset):
        updated = queryset.update(status=models.Review.Status.NOT_APPROVED)
        self.message_user(request, f'{updated} рецензий отклонено', messages.SUCCESS)

    text_display.short_description = 'Текст'
    review_pdf.short_description = 'PDF со статусом'
    approve_reviews.short_description = 'Одобрить выбранные рецензии'
    reject_reviews.short_description = 'Отклонить выбранные рецензии'
