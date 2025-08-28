from src.models.entities.connection_handler import DatabaseHandler
from src.models.entities.database import Notifications


class NotificationsRepository(DatabaseHandler):
    def __init__(self):
        super().__init__()

    def get_unread_notifications(self):
        with self:
            return (
                self.session.query(Notifications)
                .filter(Notifications.is_read == False)
                .all()
            )

    def save_notification(self, message):
        with self:
            notification = Notifications(message=message)
            self.session.add(notification)
            self.session.commit()
            return True
        return False

    def mark_as_read(self, notification: str | int):
        with self:
            if isinstance(notification, int):
                return (
                    self.session.query(Notifications)
                    .filter(Notifications.id == notification)
                    .update({"is_read": True})
                )
            return (
                self.session.query(Notifications)
                .filter(Notifications.message == notification)
                .update({"is_read": True})
            )
