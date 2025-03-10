from typing import Any

from django.views.generic.detail import BaseDetailView
from django.views.generic.list import BaseListView
from movies.api.mixins import MoviesApiMixin


class MoviesListApi(MoviesApiMixin, BaseListView):
    paginate_by = 50

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Возвращает контекст с данными для всех фильмов."""
        queryset = self.get_queryset()
        paginator, page, queryset, _ = self.paginate_queryset(
            queryset, self.paginate_by
        )

        context = {
            "count": paginator.count,
            "total_pages": paginator.num_pages,
            "prev": page.previous_page_number() if page.has_previous() else None,
            "next": page.next_page_number() if page.has_next() else None,
            "results": list(queryset),
        }
        return context


class MoviesDetailApi(MoviesApiMixin, BaseDetailView):
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Возвращает контекст с данными для одного фильма."""
        film_work = self.get_object()

        context = {
            "id": film_work["id"],
            "title": film_work["title"],
            "description": film_work["description"],
            "creation_date": film_work["creation_date"],
            "rating": film_work["rating"],
            "type": film_work["type"],
            "genres": film_work["genres"],
            "actors": film_work["actors"],
            "directors": film_work["directors"],
            "writers": film_work["writers"],
        }
        return context
