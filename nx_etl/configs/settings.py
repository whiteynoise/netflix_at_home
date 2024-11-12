from utils.pydantic_models import EnvSettings

batchsize = 250
sleep_time_etl = 600

settings = EnvSettings()

pg_config = {
    'dbname': settings.postgres_db,
    'user': settings.postgres_user,
    'password': settings.postgres_password,
    'host': settings.postgres_host,
    'port': settings.postgres_port,
}

redis_config = {
    'host': settings.redis_host,
    'port': settings.redis_port,
}

elastic_config = {
    'host': settings.elastic_host,
    'port': settings.elastic_port,
}
