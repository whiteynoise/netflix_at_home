from consumer import consumer


def start_server():
    for message in consumer:
        print(message)


if __name__ == "__main__":
    print("Server started...")
    start_server()
