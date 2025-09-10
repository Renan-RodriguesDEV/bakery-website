from sqlalchemy import text
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
                .order_by(Notifications.created_at)
                .all()
            )

    def get_count_unread_notifications(self):
        with self:
            query = self.session.execute(
                text("SELECT COUNT(id) FROM notifications WHERE is_read = false")
            )
            result = query.fetchall()
            try:
                return result[0][0] if result else 0
            except Exception as e:
                print(e)
                return 0

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


notifications_repository = NotificationsRepository()
