import commons.models.entity_models as schemes

from commons.models.settings_model import NXUgcEnvSettings

from commons.services.bookmarks import BookmarkService
from commons.services.likes import LikeService
from commons.services.ratings import RatingService
from commons.services.reviews import ReviewService


settings = NXUgcEnvSettings()

REDIS_CONFIG = {
    "host": settings.redis_host,
    "port": settings.redis_port,
}

MONGODB_CONFIG = {
    "user": settings.mongo_user,
    "password": settings.mongo_password,
    "host": settings.mongo_host,
    "port": settings.mongo_port,
}

SERVICE_INFO_BY_TOPIC: dict = {
    'ugc_ratings': {
        'service_class': RatingService,
        'service_methods_schemes': {
            'add_rating': schemes.RatingChange,
            'update_rating': schemes.RatingChange,
            'delete_rating': schemes.UserFilmBase,
        },
    },
    'ugc_reviews': {
        'service_class': ReviewService,
        'service_methods_schemes': {
            'add_review': schemes.AddReview,
            'update_review': schemes.UpdReview,
            'delete_review': schemes.UserFilmBase,
        }
    },
    'ugc_likes': {
        'service_class': LikeService,
        'service_methods_schemes': {
            'add_like': schemes.AddLike,
            'delete_like': schemes.ReviewUserBase,
        },
    },
    'ugc_bookmarks': {
        'service_class': BookmarkService,
        'service_methods_schemes': {
            'add_to_bookmark': schemes.AddToBookmark,
            'delete_from_bookmark': schemes.DelFromBookmark,
        },
    }
}

AUTH_SERVICE_URL = settings.auth_service_url
