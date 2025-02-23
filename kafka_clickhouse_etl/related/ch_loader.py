from clickhouse_driver import Client

class ClickHouseLoader:
    def __init__(self, client: Client):
        self._click_house_client = client
            
    def load_data(self, batch: list[tuple], query: str) -> None:
        """Загрузка данных в ClickHouse."""
        self._click_house_client.execute(
            query=query,
            params=batch,
        )
