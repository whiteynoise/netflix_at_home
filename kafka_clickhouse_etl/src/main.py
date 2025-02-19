from consumer import consumer
from etl_service import ETL


def start_server():
    etl: ETL = ETL(consumer=consumer)
    etl.transform()


if __name__ == "__main__":
    print("Server started...")
    start_server()
