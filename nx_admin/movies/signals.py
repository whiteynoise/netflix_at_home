import datetime

from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender="movies.FilmWork")
def attention(sender, instance, created, **kwargs):
    if created and instance.creation_date == datetime.date.today():
        print(f"Сегодня премьера {instance.title}! 🥳")
