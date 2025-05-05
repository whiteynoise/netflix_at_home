import certifi
import ssl

from abstracts import AbstractWorker, AbstractBrokerConsumer
from aiosmtplib import SMTP
from contextlib import asynccontextmanager
from email.message import EmailMessage
from jinja2 import Environment, FileSystemLoader

from configs.logger_config import logger
from configs.smtp_settings import SMTPSettings


templates = Environment(
    loader=FileSystemLoader("/app/templates"),
    auto_reload=True,
)


class MailWorker(AbstractWorker):
    def __init__(self, broker_consumer: AbstractBrokerConsumer, transfer_setup_data: dict):
        self.broker_consumer: AbstractBrokerConsumer = broker_consumer
        self.transfer_setup_data: SMTPSettings = transfer_setup_data
        self.smtp_server: SMTP | None = None

    @asynccontextmanager
    async def setup_transfer(self):
        """Подключение по SMTP к почтовому серверу."""
        logger.info("Connecting to SMTP server...")

        self.smtp_server = SMTP(
            hostname=self.transfer_setup_data.smtp_host,
            port=self.transfer_setup_data.smtp_port,
            use_tls=True,
            tls_context=ssl.create_default_context(cafile=certifi.where()),
        )

        await self.smtp_server.connect()

        await self.smtp_server.login(
            self.transfer_setup_data.sender_address,
            self.transfer_setup_data.sender_password,
        )

        logger.info("SMTP connection established")

        try:
            yield
        finally:
            await self.smtp_server.quit()

    async def process_message(self, notification_info: dict) -> None:
        """Обработка и отправка сообщения на почту."""
        rendered_msg = self.render_message(notification_info=notification_info)

        message = EmailMessage()
        message["From"] = self.transfer_setup_data.sender_address
        message["To"] = notification_info['recipient_data']['email']
        message["Subject"] = notification_info['subject']

        message.add_alternative(rendered_msg, subtype='html')

        await self.smtp_server.send_message(message)
        logger.info("The message has been sent")

    async def start_worker(self) -> None:
        """Точка входа в воркер."""
        logger.info("Wake up, samurai, we have mail to send...")
        async with self.setup_transfer():
            await self.broker_consumer.start_consumption(callback=self.process_message)

    @staticmethod
    def render_message(notification_info: dict) -> str:
        """Рендер сообщения по выбранному шаблону."""
        template = templates.get_template(notification_info['template_name'])
        return template.render(**notification_info['recipient_data'])
