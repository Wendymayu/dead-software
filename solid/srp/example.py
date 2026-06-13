"""单一职责原则 (SRP) 最小化示例

演示一个类承担多职责 vs 多个类各担一职：
- BadClass 同时处理用户管理、邮件发送、日志记录
- GoodClasses 各自只负责一项职责
- 一个变更原因不应影响其他功能
"""


# --- 违反 SRP ---
class BadClass:
    """一个类做三件事：用户管理 + 邮件 + 日志"""
    def create_user(self, name):
        print(f"[Bad] 创建用户: {name}")
        print(f"[Bad] 发送欢迎邮件给 {name}")
        print(f"[Bad] 记录日志: 创建用户 {name}")

    def send_email(self, to, body):
        print(f"[Bad] 发送邮件给 {to}: {body}")
        print(f"[Bad] 记录日志: 发送邮件给 {to}")

    def log_activity(self, action):
        print(f"[Bad] 记录日志: {action}")


# --- 遵循 SRP ---
class UserManager:
    """只负责用户管理"""
    def create_user(self, name):
        print(f"[Good] 创建用户: {name}")


class EmailService:
    """只负责邮件发送"""
    def send_email(self, to, body):
        print(f"[Good] 发送邮件给 {to}: {body}")


class ActivityLogger:
    """只负责日志记录"""
    def log(self, action):
        print(f"[Good] 记录日志: {action}")


# --- 运行演示 ---
if __name__ == "__main__":
    print("=" * 40)
    print("SRP 演示：单一职责原则")
    print("=" * 40 + "\n")

    print("--- 违反 SRP (BadClass) ---")
    bad = BadClass()
    bad.create_user("Alice")
    print()

    print("--- 遵循 SRP (GoodClasses) ---")
    user_mgr = UserManager()
    email_svc = EmailService()
    logger = ActivityLogger()

    user_mgr.create_user("Alice")
    email_svc.send_email("Alice", "欢迎加入!")
    logger.log("创建用户 Alice")
    print()

    print("关键区别：BadClass 修改邮件逻辑会影响用户管理")
    print("GoodClasses 各类独立修改，互不影响")
