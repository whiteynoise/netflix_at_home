from abstracts import AbstractWorker


class BaseWorker():
    def __init__(
        self,
        service_class: object,
        service_methods_schemes: dict,
    ):
        self.service_class = service_class
        self.service_methods_schemes = service_methods_schemes

    async def __call__(self, message: dict) -> None:
        message_method = message['method']

        method = getattr(self.service_class, message_method)
        scheme = self.service_methods_schemes.get(message_method)

        await method(scheme(**message['payload']))
