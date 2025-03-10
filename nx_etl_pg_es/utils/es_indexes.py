base_index_settings = {
    "refresh_interval": "1s",
    "analysis": {
        "filter": {
            "english_stop": {"type": "stop", "stopwords": "_english_"},
            "english_stemmer": {"type": "stemmer", "language": "english"},
            "english_possessive_stemmer": {
                "type": "stemmer",
                "language": "possessive_english",
            },
            "russian_stop": {"type": "stop", "stopwords": "_russian_"},
            "russian_stemmer": {"type": "stemmer", "language": "russian"},
        },
        "analyzer": {
            "ru_en": {
                "tokenizer": "standard",
                "filter": [
                    "lowercase",
                    "english_stop",
                    "english_stemmer",
                    "english_possessive_stemmer",
                    "russian_stop",
                    "russian_stemmer",
                ],
            }
        },
    },
}

movies_index = {
    "dynamic": "strict",
    "properties": {
        "id": {"type": "keyword"},
        "imdb_rating": {"type": "float"},
        "genres": {"type": "keyword"},
        "title": {
            "type": "text",
            "analyzer": "ru_en",
            "fields": {"raw": {"type": "keyword"}},
        },
        "description": {"type": "text", "analyzer": "ru_en"},
        "directors_names": {"type": "text", "analyzer": "ru_en"},
        "actors_names": {"type": "text", "analyzer": "ru_en"},
        "writers_names": {"type": "text", "analyzer": "ru_en"},
        "directors": {
            "type": "nested",
            "dynamic": "strict",
            "properties": {
                "id": {"type": "keyword"},
                "name": {"type": "text", "analyzer": "ru_en"},
            },
        },
        "actors": {
            "type": "nested",
            "dynamic": "strict",
            "properties": {
                "id": {"type": "keyword"},
                "name": {"type": "text", "analyzer": "ru_en"},
            },
        },
        "writers": {
            "type": "nested",
            "dynamic": "strict",
            "properties": {
                "id": {"type": "keyword"},
                "name": {"type": "text", "analyzer": "ru_en"},
            },
        },
    },
}

genres_index = {
    "dynamic": "strict",
    "properties": {
        "id": {"type": "keyword"},
        "name": {"type": "text", "analyzer": "ru_en"},
        "description": {"type": "text", "analyzer": "ru_en"},
    },
}

persons_index = {
    "dynamic": "strict",
    "properties": {
        "id": {"type": "keyword"},
        "name": {"type": "text", "analyzer": "ru_en"},
        "films": {
            "type": "nested",
            "dynamic": "strict",
            "properties": {
                "id": {"type": "keyword"},
                "roles": {"type": "text", "analyzer": "ru_en"},
            },
        },
    },
}

index_by_name = {
    "movies": movies_index,
    "genres": genres_index,
    "persons": persons_index,
}
