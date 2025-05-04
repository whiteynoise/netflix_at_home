import requests
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from movies.models import (CustomUser, FilmWork, Genre, GenreFilmWork, Person,
                           PersonFilmWork)

from constants import TEMPLATE_ID, MASSIVE_NOTIFICATION_SERVICE_API


class GenreFilmWorkInline(admin.TabularInline):
    model = GenreFilmWork
    autocomplete_fields = ("genre", "film_work")


class PersonFilmWorkInline(admin.TabularInline):
    model = PersonFilmWork
    autocomplete_fields = ("person", "film_work")


@admin.register(FilmWork)
class FilmWorkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmWorkInline, PersonFilmWorkInline)
    list_display = ("title", "type", "creation_date", "rating", "get_genres")
    list_filter = ("type", "creation_date", "genres")
    search_fields = ("title", "description", "id")

    def get_genres(self, obj):
        return ",".join([genre.name for genre in obj.genres.all()])

    def get_queryset(self, request):
        queryset = super().get_queryset(request).prefetch_related("genres")
        return queryset

    get_genres.short_description = _("genre")

    def save_model(self, request, obj, form, change):
        is_new = obj.pk is None
        super().save_model(request, obj, form, change)

        if is_new:
            try:
                body = {
                    "template_id": TEMPLATE_ID,
                    "title": f"Новый фильм: {obj.title}",
                    "description": f"Фильм добавлен: {obj.description or ''}",
                    "time": now().isoformat(),
                    "notification_type": "email",
                    "volume_type": "massive",
                    "roles": ["base_user"],
                }
                response = requests.post(
                    MASSIVE_NOTIFICATION_SERVICE_API,
                    json=body,
                    timeout=3,
                )
                if response.status_code not in (200, 201):
                    self.message_user(request, f"Ошибка отправки уведомления: {response.status_code}", level='warning')
            except Exception as e:
                self.message_user(request, f"Ошибка уведомления: {e}", level='warning')


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    inlines = (PersonFilmWorkInline,)

    list_display = ("full_name",)
    search_fields = ("full_name",)


admin.site.register(CustomUser, UserAdmin)
