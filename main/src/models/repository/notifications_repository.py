from sqlalchemy import text
from src.models.entities.connection_handler import DatabaseHandler
from src.models.entities.database import Notifications, Product


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

    def save_notification(self, message, fk_product):
        with self:
            notification = Notifications(message=message, fk_product=fk_product)
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
            if not notification:
                return False
            product = (
                self.session.query(Product)
                .filter(Product.id == notification.fk_product)
                .first()
            )
            notification.is_read = True
            product.in_queue = False
            self.session.commit()
            self.session.refresh(notification)
            return True
        return False


notifications_repository = NotificationsRepository()
