from pydantic import BaseModel


class NotificationMessage(BaseModel):
    subject: str
    user_id: str
    recipient_data: dict
    template_name: str | None
    msg_text: str | None
