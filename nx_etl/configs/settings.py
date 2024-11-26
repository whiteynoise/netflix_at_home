from configs.setting_model import EnvSettings

settings = EnvSettings()

pg_config = {
    "dbname": settings.postgres_db,
    "user": settings.postgres_user,
    "password": settings.postgres_password,
    "host": settings.postgres_host,
    "port": settings.postgres_port,
}

redis_config = {
    "host": settings.redis_host,
    "port": settings.redis_port,
}

elastic_config = {
    "host": settings.elastic_host,
    "port": settings.elastic_port,
}
