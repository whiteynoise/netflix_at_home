insert_user_events: str = """
    INSERT INTO default.user_events (
        user_event_tag,
        user_id,
        event_time
    )
    VALUES
"""

insert_film_events: str = """
    INSERT INTO default.film_events (
        film_event_tag,
        film_id,
        user_id,
        event_time
    )
    VALUES
"""

queries_by_topic = {"user": insert_user_events, "film": insert_film_events}
