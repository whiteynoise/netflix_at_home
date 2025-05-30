import commons.services as services
import commons.models.entity_models as schemes

from commons.models.settings_model import NXUgcEnvSettings


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
        'service_class': services.RatingService,
        'service_methods_schemes': {
            'add_rating': schemes.RatingChange,
            'update_rating': schemes.RatingChange,
            'delete_rating': schemes.UserFilmBase,
        },
    },
    'ugc_reviews': {
        'service_class': services.ReviewService,
        'service_methods_schemes': {
            'add_review': schemes.AddReview,
            'update_review': schemes.UpdReview,
            'delete_review': schemes.UserFilmBase,
        }
    },
    'ugc_likes': {
        'service_class': services.LikeService,
        'service_methods_schemes': {
            'add_like': schemes.AddLike,
            'delete_like': schemes.ReviewUserBase,
        },
    },
    'ugc_bookmarks': {
        'service_class': services.BookmarkService,
        'service_methods_schemes': {
            'add_to_bookmark': schemes.AddToBookmark,
            'delete_from_bookmark': schemes.DelFromBookmark,
        },
    }
}

AUTH_SERVICE_URL = settings.auth_service_url
