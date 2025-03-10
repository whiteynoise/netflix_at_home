from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from movies.models import (CustomUser, FilmWork, Genre, GenreFilmWork, Person,
                           PersonFilmWork)


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
