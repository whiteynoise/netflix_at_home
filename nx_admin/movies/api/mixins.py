from typing import Any

from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q, Value
from django.db.models.functions import Coalesce
from django.db.models.query import QuerySet
from django.http import JsonResponse
from movies.models import FilmWork


class MoviesApiMixin:
    model = FilmWork
    http_method_names = ["get"]

    def get_queryset(self) -> QuerySet[Any]:
        """Возвращает объект фильма со всеми его данными:
        инфо о фильме, участниками и жанрами (в виде списка)"""

        return (
            FilmWork.objects.values(
                "id",
                "title",
                "description",
                "creation_date",
                "rating",
                "type",
            )
            .annotate(
                genres=ArrayAgg("genres__name", distinct=True),
                actors=Coalesce(
                    ArrayAgg(
                        "persons__full_name",
                        filter=Q(personfilmwork__role="actor"),
                        distinct=True,
                    ),
                    Value([]),
                ),
                directors=Coalesce(
                    ArrayAgg(
                        "persons__full_name",
                        filter=Q(personfilmwork__role="director"),
                        distinct=True,
                    ),
                    Value([]),
                ),
                writers=Coalesce(
                    ArrayAgg(
                        "persons__full_name",
                        filter=Q(personfilmwork__role="writer"),
                        distinct=True,
                    ),
                    Value([]),
                ),
            )
            .order_by("title")
        )

    def render_to_response(self, context, **response_kwargs: Any):
        return JsonResponse(context)
