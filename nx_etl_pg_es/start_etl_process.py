from related.es_loader import ESLoader
from related.pg_extractor import PGExtractor

from related.storage import RedisStateStorage
from configs.settings import redis_config, pg_config, elastic_config
from related.etl import Etl, PostgresToEsEtl

from related.es_loader import Loader
from related.pg_extractor import Extractor
from related.storage import KeyValueStorage


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
