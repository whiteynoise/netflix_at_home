import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger
from datetime import datetime

from constants import MASSIVE_NOTIFICATION_SERVICE_API, TEMPLATE_ID
from models.response import CreateEventSchema
from session import aiohttp_session

scheduler = AsyncIOScheduler()


def schedule_event(event: CreateEventSchema):
    """Отложенное однократное событие"""

    async def task():
        """Таска"""
        async with aiohttp_session.post(
            MASSIVE_NOTIFICATION_SERVICE_API, json=event.model_dump()
        ) as response:
            if response.status not in (200, 201):
                print(
                    f"Ошибка при отправки события {event.model_dump()}: {response.status}"
                )
                return

    trigger = DateTrigger(run_date=event.time)
    scheduler.add_job(task, trigger)


def schedule_biweekly_film_fetch():
    """Периодическая задача"""

    trigger = CronTrigger(
        day_of_week="sun", hour=9, minute=0, second=0, timezone="UTC", week="2" # каждые две недели
    )

    async def fetch_films_task():
        body = {
            "template_id": TEMPLATE_ID,
            "title": f"Топ-фильмов за две недели {datetime.now().isoformat()}",
            "description": "События топ-фильмов за две недели!",
            "time": datetime.now().isoformat(),
            "volume_type": "massive",
            "roles": ["base_user"],
        }
        async with aiohttp_session.post(
            MASSIVE_NOTIFICATION_SERVICE_API, json=body
        ) as response:
            if response.status not in (200, 201):
                print(
                    f" Ошибка при отправки события на топ-фильмов месяца: {response.status}"
                )
                return

    scheduler.add_job(fetch_films_task, trigger, name="top_films")


def start_scheduler():
    scheduler.start()
