"""六边形架构 (Hexagonal Architecture) 最小化示例

演示端口与适配器模式：
- 核心业务逻辑定义端口（抽象接口）
- 适配器实现端口，连接外部系统
- 业务逻辑只依赖端口，不依赖具体适配器"""

from abc import ABC, abstractmethod


# --- 端口(Port)：核心声明它需要什么接口 ---
class Repository(ABC):
    """数据存储端口 — 核心只声明需要存取用户，不关心怎么存"""
    @abstractmethod
    def save(self, user): pass
    @abstractmethod
    def find(self, name): pass


class NotificationPort(ABC):
    """通知端口 — 核心只声明需要发送消息，不关心发到哪里"""
    @abstractmethod
    def send(self, message): pass


# --- 核心业务逻辑：只使用端口，绝不引用适配器 ---
class UserService:
    """核心业务 — 依赖抽象端口而非具体实现"""
    def __init__(self, repo: Repository, notifier: NotificationPort):
        self.repo = repo      # 注入的是端口，不是适配器
        self.notifier = notifier

    def register(self, name):
        if self.repo.find(name):
            self.notifier.send(f"用户 {name} 已存在，注册失败")
            return
        self.repo.save({"name": name})
        self.notifier.send(f"用户 {name} 注册成功")


# --- 适配器(Adapter)：外部系统实现端口 ---
class InMemoryRepo(Repository):
    """内存适配器 — 开发/测试时用，用字典模拟存储"""
    def __init__(self):
        self._data = {}
    def save(self, user):
        self._data[user["name"]] = user
        print(f"  [InMemoryRepo] 已保存: {user['name']}")
    def find(self, name):
        return self._data.get(name)


class ConsoleNotifier(NotificationPort):
    """控制台适配器 — 将通知输出到终端"""
    def send(self, message):
        print(f"  [ConsoleNotifier] 通知: {message}")


# --- 运行演示 ---
if __name__ == "__main__":
    # 适配器从外部注入 — 核心完全不知道用了什么实现
    service = UserService(InMemoryRepo(), ConsoleNotifier())

    print("=" * 40)
    print("六边形架构演示：核心通过端口与外部交互")
    print("=" * 40 + "\n")

    service.register("Alice")
    print()
    service.register("Alice")  # 重复注册，触发"已存在"通知
