from time import sleep
from typing import Protocol

from configs.logger_config import logger
from related.es_loader import Loader
from related.pg_extractor import Extractor
from related.storage import KeyValueStorage


class Etl(Protocol):
    def start_etl_process(self):
        """Начинает процесс etl"""


class PostgresToEsEtl:
    def __init__(
        self,
        extractor: Extractor,
        loader: Loader,
        state: KeyValueStorage,
        sleep_time_etl: int = 600,
    ):
        self.extractor = extractor
        self.loader = loader
        self.state = state
        self.sleep_time_etl = sleep_time_etl

    def start_etl_process(self):
        """Начинает процесс etl"""

        logger.info("Start preparing env loader!")
        self.loader.prepare()
        logger.info("Prepare loaders env ready!")

        logger.info("Wake up, samurai, we have data to sync...")
        while True:
            self.etl_process()

    def etl_process(self) -> None:
        """ETL процесс"""
        current_date: str = self.state.get_state()

        if next_date_state := self.extractor.check_on_update(current_date):
            for index_name in self.loader.indexes.keys():
                for batch in self.extractor.get_data(index_name, current_date):
                    self.loader.save_data(batch, index_name)

            self.state.set_state(next_date_state)
        else:
            logger.info("No new data to load.")

        logger.info("I'm going to sleep for %s seconds.", self.sleep_time_etl)
        sleep(self.sleep_time_etl)
