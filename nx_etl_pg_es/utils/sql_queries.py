def get_max_time_across_tables(redis_date) -> str:
    return f"""
        SELECT max(max_mod) as new_date
        FROM (
            SELECT max(modified) as max_mod
            FROM content.film_work
            WHERE modified > '{redis_date}'::timestamp
            UNION
            SELECT max(g.modified) as max_mod
            FROM content.genre g
            JOIN content.genre_film_work gfw ON g.id = gfw.genre_id
            WHERE g.modified > '{redis_date}'::timestamp
            UNION
            SELECT max(p.modified) as max_mod
            FROM content.person p
            JOIN content.person_film_work gfw ON p.id = gfw.person_id
            WHERE p.modified > '{redis_date}'::timestamp
        ) AS max_mod_across_tables
    """


def get_filmworks(redis_date) -> str:
    return f"""
        SELECT
            fw.id,
            fw.title,
            fw.description,
            fw.rating AS imdb_rating,
            fw.type,
            coalesce(array_agg(DISTINCT g.name), '{{}}') AS genres,
            coalesce(array_agg(DISTINCT p.full_name) FILTER (WHERE pfw.role = 'actor'), '{{}}') AS actors_names,
            coalesce(array_agg(DISTINCT p.full_name) FILTER (WHERE pfw.role = 'writer'), '{{}}') AS writers_names,
            coalesce(array_agg(DISTINCT p.full_name) FILTER (WHERE pfw.role = 'director'), '{{}}') AS directors_names,
            coalesce(json_agg(
                DISTINCT jsonb_build_object(
                    'id', p.id,
                    'name', p.full_name
                )
            ) FILTER (WHERE p.id is not null AND pfw.role = 'director'), '[]') AS directors,
             coalesce(json_agg(
                DISTINCT jsonb_build_object(
                    'id', p.id,
                    'name', p.full_name
                )
            ) FILTER (WHERE p.id is not null AND pfw.role = 'actor'), '[]') AS actors,
             coalesce(json_agg(
                DISTINCT jsonb_build_object(
                    'id', p.id,
                    'name', p.full_name
                )
            ) FILTER (WHERE p.id is not null AND pfw.role = 'writer'), '[]') AS writers
        FROM content.film_work fw
        LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
        LEFT JOIN content.person p ON p.id = pfw.person_id
        LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
        LEFT JOIN content.genre g ON g.id = gfw.genre_id
        WHERE fw.modified > '{redis_date}'::timestamp or
              p.modified > '{redis_date}'::timestamp or
              g.modified > '{redis_date}'::timestamp
        GROUP BY fw.id
    """


def get_genres(redis_date) -> str:
    return f"""
        SELECT
            g.id,
            g.name,
            g.description
        FROM content.genre g
        WHERE g.modified > '{redis_date}'::timestamp
        GROUP BY g.id
    """


def get_persons(redis_date) -> str:
    return f"""
        WITH pfw_agg AS (
            SELECT
                pfw.person_id,
                pfw.film_work_id,
                array_agg(DISTINCT pfw.role) AS roles
            FROM content.person_film_work pfw
            GROUP BY pfw.person_id, pfw.film_work_id
        )
        SELECT
            pfw.person_id as id,
            p.full_name as name,
            coalesce(
                json_agg(DISTINCT
                    jsonb_build_object(
                        'id', pfw.film_work_id,
                        'roles', pfw.roles
                )
            ), '[]') AS films
        FROM pfw_agg AS pfw
        JOIN content.person p ON p.id = pfw.person_id
        WHERE p.modified > '{redis_date}'::timestamp
        GROUP BY pfw.person_id, p.full_name;
    """


quaries_by_index: dict = {
    "movies": get_filmworks,
    "genres": get_genres,
    "persons": get_persons,
}
