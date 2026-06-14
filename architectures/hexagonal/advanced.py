"""六边形架构进阶示例：模拟 Spring Boot 端口与适配器

展示 Spring Boot 六边形架构核心：
- Core: UserService 纯业务，定义 Port 接口
- Driving: RestController (入站) 调用核心
- Driven: JpaUserRepo / EmailNotifier (出站) 实现 Port
- Spring DI: 适配器注入核心，核心不依赖适配器
"""

from abc import ABC, abstractmethod


# --- Core Domain: 只依赖端口接口 ---
class UserRepositoryPort(ABC):
    @abstractmethod
    def find_by_email(self, email): pass
    @abstractmethod
    def save(self, user): pass

class NotificationPort(ABC):
    @abstractmethod
    def send(self, email, subject, body): pass

class UserService:
    """核心业务: 只依赖端口接口，不依赖具体实现"""
    def __init__(self, repo: UserRepositoryPort, notifier: NotificationPort):
        self.repo = repo
        self.notifier = notifier

    def register(self, email, name):
        print(f"[Core] UserService.register({email}, {name})")
        if self.repo.find_by_email(email):
            print("  [Core] 拒绝: 用户已存在")
            return False
        user = {"email": email, "name": name}
        self.repo.save(user)
        self.notifier.send(email, "注册成功", f"{name}, 欢迎加入!")
        print("  [Core] 注册完成")
        return True


# --- Driving Adapter: REST 入站适配器 ---
class RestController:
    def __init__(self, service: UserService):
        self.service = service

    def post_register(self, email, name):
        print(f"[REST] POST /api/users/register  {email}/{name}")
        ok = self.service.register(email, name)
        print(f"  [REST] HTTP {201 if ok else 409}")
        return 201 if ok else 409


# --- Driven Adapters: 出站适配器，实现端口 ---
class JpaUserRepository(UserRepositoryPort):
    def __init__(self):
        self._db = {}

    def find_by_email(self, email):
        found = self._db.get(email)
        print(f"  [JPA] find({email}) → {found or 'null'}")
        return found

    def save(self, user):
        self._db[user["email"]] = user
        print(f"  [JPA] save → {user['email']} 入库")

class EmailNotifier(NotificationPort):
    def send(self, email, subject, body):
        print(f"  [Email] 发送 → {email}: [{subject}] {body}")

class LogNotifier(NotificationPort):
    """日志替代邮件（测试），核心零修改"""
    def send(self, email, subject, body):
        print(f"  [Log] 记录 → {email}: [{subject}] {body}")


# --- Spring DI 组装 ---
def bootstrap(prod=True):
    """模拟 @SpringBootApplication: 适配器注入核心"""
    repo = JpaUserRepository()
    notifier = EmailNotifier() if prod else LogNotifier()
    return RestController(UserService(repo, notifier))

if __name__ == "__main__":
    print("=" * 50)
    print("Spring Boot 六边形架构模拟")
    print("=" * 50 + "\n")

    print("--- 生产: JPA + Email ---")
    app = bootstrap(prod=True)
    app.post_register("alice@test.com", "Alice")
    app.post_register("alice@test.com", "Alice2")  # 重复

    print("\n--- 开发: JPA + Log (换适配器，核心不变) ---")
    app_dev = bootstrap(prod=False)
    app_dev.post_register("bob@test.com", "Bob")
