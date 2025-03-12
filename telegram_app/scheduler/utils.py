from scheduler.handlers.notifications.event_notification import EventNotificator
from scheduler.handlers.notifications.game_notification import GameNotificator


async def send_notifications():
    notificator = GameNotificator()
    await notificator.run()

    notificator = EventNotificator()
    await notificator.run()
