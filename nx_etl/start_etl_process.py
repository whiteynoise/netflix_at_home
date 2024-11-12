from time import sleep

from related.es_loader import ESLoader
from related.pg_extractor import PGExtractor
from related.state import RedisStateStorage

from configs.logger_config import logger
from configs.settings import batchsize, sleep_time_etl

from utils.es_indexes import index_by_name


def etl_process() -> None:
    """Процесс переливки данных из PG в ES."""
    current_date: str = state.get_state()

    if next_date_state := extractor.check_on_update(current_date):
        for index_name in index_by_name.keys():
            for batch in extractor.get_data(index_name, current_date, batchsize):
                loader.save_data(batch, index_name)

        state.set_state(next_date_state)
    else:
        logger.info("No new data to load.")
    
    logger.info("I'm going to sleep for %s seconds.", sleep_time_etl)

    sleep(sleep_time_etl)


if __name__ == '__main__':
    extractor = PGExtractor()
    loader = ESLoader()
    state = RedisStateStorage()

    for index_name, index_mapping in index_by_name.items():
        loader.create_index_if_not_exists(index_name, index_mapping)

    logger.info("Wake up, samurai, we have data to sync...")

    while True:
        etl_process()
