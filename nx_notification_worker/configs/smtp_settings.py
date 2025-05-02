from pydantic_settings import BaseSettings, SettingsConfigDict


class SMTPSettings(BaseSettings):
    smtp_host: str
    smtp_port: str
    sender_address: str
    sender_password: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


transfer_setup_data = SMTPSettings()
