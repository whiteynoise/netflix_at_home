import uuid

from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from movies.mixins import TimeStampedMixin, UUIDMixin


class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField(_("genre name"), max_length=255, unique=True)
    description = models.TextField(_("description"), blank=True, null=True)

    class Meta:
        verbose_name = _("Genre")
        verbose_name_plural = _("Genres")

        indexes = [models.Index(fields=["name"], name="genre_name_idx")]

    def __str__(self):
        return self.name


class GenreFilmWork(UUIDMixin):
    film_work = models.ForeignKey(
        "FilmWork", on_delete=models.CASCADE, verbose_name=_("Film work")
    )
    genre = models.ForeignKey(
        "Genre", on_delete=models.CASCADE, verbose_name=_("Genre")
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Genre of film")
        verbose_name_plural = _("Genres of film")

        constraints = [
            models.UniqueConstraint(
                fields=["film_work", "genre"], name="genre_film_work_idx"
            )
        ]

    def __str__(self):
        return str(self.created_at)


class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.CharField(_("full name"), max_length=255)

    class Meta:
        verbose_name = _("Person")
        verbose_name_plural = _("Persons")

        indexes = [models.Index(fields=["full_name"], name="person_full_name_idx")]

    def __str__(self):
        return self.full_name


class PersonFilmWork(UUIDMixin):
    class Roles(models.TextChoices):
        ACTOR = ("actor", _("Actor"))
        WRITER = ("writer", _("Writer"))
        DIRECTOR = ("director", _("Director"))

    film_work = models.ForeignKey(
        "FilmWork", on_delete=models.CASCADE, verbose_name=_("Film work")
    )
    person = models.ForeignKey(
        "Person", on_delete=models.CASCADE, verbose_name=_("Person")
    )
    role = models.CharField(
        _("role"), choices=Roles.choices, default=Roles.ACTOR, max_length=255
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Participation in the cinema")
        verbose_name_plural = _("Participation in the cinema")

        constraints = [
            models.UniqueConstraint(
                fields=["film_work", "person", "role"], name="film_work_person_role_idx"
            )
        ]

    def __str__(self):
        return self.role


class FilmWork(UUIDMixin, TimeStampedMixin):
    class FilmTypes(models.TextChoices):
        MOVIE = ("movie", _("Movie"))
        TV_SHOW = ("tv_show", _("TV Show"))

    title = models.CharField(_("title"), max_length=255)
    description = models.TextField(_("description"), blank=True, null=True)
    creation_date = models.DateField(_("creation date"), blank=True, null=True)
    file_path = models.FileField(
        _("file path"),
        upload_to="movies/",
        blank=True,
        null=True,
    )
    rating = models.FloatField(
        _("rating"),
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    type = models.CharField(
        _("type"), max_length=150, choices=FilmTypes.choices, default=FilmTypes.MOVIE
    )
    genres = models.ManyToManyField(
        Genre,
        through="GenreFilmWork",
        related_name="film_works",
        verbose_name=_("genres"),
    )
    persons = models.ManyToManyField(
        Person,
        through="PersonFilmWork",
        related_name="film_works",
        verbose_name=_("persons"),
    )

    class Meta:
        verbose_name = _("Film work")
        verbose_name_plural = _("Film works")

        indexes = [
            models.Index(fields=["title"], name="film_work_title_idx"),
            models.Index(fields=["rating"], name="film_work_rating_idx"),
            models.Index(fields=["creation_date"], name="film_work_creation_date_idx"),
        ]

    def __str__(self):
        return f"{self.title}, {self.creation_date}"


class CustomUser(AbstractUser):
    """Кастомный пользователь"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.username
