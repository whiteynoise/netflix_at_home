import typer
from asyncio import run as aiorun
from db.postgres import async_session
from models.entity import Users
from sqlalchemy import select

app = typer.Typer(help="CLI создания супер пользователя.")


async def _create_super_user(username: str, password: str, email: str) -> None:
    """
    Создание супер пользователя.
    """
    async with async_session() as db:
        result = await db.execute(select(Users).filter(Users.username == username))
        user_exists = result.scalars().first()

        if not user_exists:
            user = Users(
                username=username, password=password, email=email, is_superuser=True
            )
            db.add(user)
            await db.commit()
            typer.echo("Пользователь создан")
        else:
            typer.echo("Пользователь с таким ником уже существует")


@app.command()
def create_super_user(username: str, password: str, email: str):
    aiorun(_create_super_user(username=username, password=password, email=email))


if __name__ == "__main__":
    app()
