from pydantic import AliasChoices, BaseModel, EmailStr, Field


class UniUserOAuth(BaseModel):
    username: str = Field(validation_alias=AliasChoices("username", "login"))
    email: EmailStr | None = Field(
        validation_alias=AliasChoices("email", "default_email")
    )
