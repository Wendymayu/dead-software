"""分层架构进阶示例：引入依赖反转

展示如何通过抽象接口实现依赖反转(DIP)，
使业务层不再直接依赖数据层的具体实现。
"""

from abc import ABC, abstractmethod


# --- 抽象接口：业务层定义它需要的数据访问能力 ---
class UserRepository(ABC):
    @abstractmethod
    def get_user(self, user_id): ...

    @abstractmethod
    def save_user(self, user_id, data): ...


# --- 数据层：实现抽象接口 ---
class InMemoryUserRepo(UserRepository):
    def __init__(self):
        self._users = {"alice": {"name": "Alice", "age": 30}}

    def get_user(self, user_id):
        print(f"  [InMemoryRepo] 查询: {user_id}")
        return self._users.get(user_id)

    def save_user(self, user_id, data):
        print(f"  [InMemoryRepo] 保存: {user_id}")
        self._users[user_id] = data


class JsonFileUserRepo(UserRepository):
    """模拟JSON文件存储（实际应读写文件，此处简化）"""

    def get_user(self, user_id):
        print(f"  [JsonFileRepo] 从文件查询: {user_id}")
        return {"name": user_id.capitalize(), "age": 99}

    def save_user(self, user_id, data):
        print(f"  [JsonFileRepo] 写入文件: {user_id}")


# --- 业务层：只依赖抽象接口，不依赖具体实现 ---
class UserService:
    def __init__(self, repo: UserRepository):  # 依赖注入
        self.repo = repo

    def get_info(self, user_id):
        print(f" [UserService] 查询: {user_id}")
        user = self.repo.get_user(user_id)
        return f"{user['name']}, 年龄 {user['age']}" if user else "不存在"


# --- 展示层 ---
class UserView:
    def __init__(self, service):
        self.service = service

    def show(self, user_id):
        print(f"[UserView] 展示: {user_id}")
        print(f"   → {self.service.get_info(user_id)}\n")


# --- 运行演示：同一业务逻辑，切换不同数据实现 ---
if __name__ == "__main__":
    print("=" * 50)
    print("进阶演示：依赖反转 — 业务层不依赖具体数据实现")
    print("=" * 50 + "\n")

    # 使用内存存储
    print("--- 使用 InMemoryUserRepo ---")
    view1 = UserView(UserService(InMemoryUserRepo()))
    view1.show("alice")

    # 切换为文件存储，业务层代码无需修改
    print("--- 切换为 JsonFileUserRepo（业务层代码不变）---")
    view2 = UserView(UserService(JsonFileUserRepo()))
    view2.show("alice")
