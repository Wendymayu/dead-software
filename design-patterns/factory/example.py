"""工厂模式 (Factory Pattern) 最小化示例

演示对象创建逻辑的集中管理：
- 工厂根据参数决定创建哪种对象
- 调用者无需知道具体类名，只与抽象接口交互
- 新增产品类型只需修改工厂
"""

from abc import ABC, abstractmethod


class Notification(ABC):
    @abstractmethod
    def send(self, message): ...


class EmailNotification(Notification):
    def send(self, message):
        print(f"    [Email] 发送邮件: {message}")


class SMSNotification(Notification):
    def send(self, message):
        print(f"    [SMS] 发送短信: {message}")


class PushNotification(Notification):
    def send(self, message):
        print(f"    [Push] 发送推送: {message}")


class NotificationFactory:
    """工厂：根据类型创建通知对象"""

    _types = {
        "email": EmailNotification,
        "sms": SMSNotification,
        "push": PushNotification,
    }

    def create(self, notification_type):
        print(f"  [Factory] 创建通知: type={notification_type}")
        cls = self._types.get(notification_type)
        if not cls:
            raise ValueError(f"未知通知类型: {notification_type}")
        return cls()


# --- 运行演示 ---
if __name__ == "__main__":
    print("=" * 40)
    print("工厂模式演示：根据类型创建不同通知对象")
    print("=" * 40 + "\n")

    factory = NotificationFactory()
    msg = "您的订单已发货"

    for type_name in ["email", "sms", "push"]:
        notification = factory.create(type_name)
        notification.send(msg)
        print()

    # 尝试创建未知类型
    try:
        factory.create("unknown")
    except ValueError as e:
        print(f"错误捕获: {e}")
