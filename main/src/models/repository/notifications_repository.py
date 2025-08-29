from src.models.entities.connection_handler import DatabaseHandler
from src.models.entities.database import Notifications


class NotificationsRepository(DatabaseHandler):
    def __init__(self):
        super().__init__()

    def get_unread_notifications(self):
        with self:
            return (
                self.session.query(Notifications)
                .filter(Notifications.is_read == False)  # noqa: E712
                .all()
            )

    def save_notification(self, message):
        with self:
            notification = Notifications(message=message)
            self.session.add(notification)
            self.session.commit()
            return True
        return False

    def mark_as_read(self, notification_id: int):
        with self:
            notification = (
                self.session.query(Notifications)
                .filter(Notifications.id == notification_id)
                .first()
            )

            notification.is_read = True
            self.session.commit()
            self.session.refresh(notification)
            return True
        return False
