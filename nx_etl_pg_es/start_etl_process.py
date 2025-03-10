import sentry_sdk
from configs.settings import (elastic_config, pg_config, redis_config,
                              sentry_dsn)
from related.es_loader import ESLoader, Loader
from related.etl import Etl, PostgresToEsEtl
from related.pg_extractor import Extractor, PGExtractor
from related.storage import KeyValueStorage, RedisStateStorage


class ETLProcess:
    """Класс для инициализации ETL"""

    def __init__(self, extract_config: dict, loader_config: dict, storage_config: dict):
        self.extract_config = extract_config
        self.loader_config = loader_config
        self.storage_config = storage_config

    def initialize(
        self,
        extractor: Extractor,
        loader: Loader,
        state: KeyValueStorage,
        Etl: Etl,
        *args,
        **kwargs,
    ):
        self.extractor = extractor(self.extract_config)
        self.loader = loader(self.loader_config)
        self.state = state(self.storage_config)

        self.Etl = Etl(self.extractor, self.loader, self.state, *args, **kwargs)

    def start(self):
        self.Etl.start_etl_process()


if __name__ == "__main__":
    sentry_sdk.init(sentry_dsn)

    etl_process = ETLProcess(
        pg_config,
        elastic_config,
        redis_config,
    )

    etl_process.initialize(
        PGExtractor,
        ESLoader,
        RedisStateStorage,
        PostgresToEsEtl,
    )
    etl_process.start()
