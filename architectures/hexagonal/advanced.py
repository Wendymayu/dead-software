"""六边形架构进阶示例：适配器替换与驱动适配器

展示六边形架构的核心优势：
- 同一端口可插拔不同适配器，核心代码零修改
- 驱动适配器从外部调用核心，核心不关心调用来源"""

from abc import ABC, abstractmethod
import os


# --- 端口(Port) ---
class Repository(ABC):
    @abstractmethod
    def save(self, user): pass
    @abstractmethod
    def find(self, name): pass


# --- 核心业务逻辑（与基础示例完全相同） ---
class UserService:
    def __init__(self, repo: Repository):
        self.repo = repo

    def register(self, name):
        if self.repo.find(name):
            print(f"  [核心] 用户 {name} 已存在")
            return False
        self.repo.save({"name": name})
        print(f"  [核心] 用户 {name} 注册成功")
        return True


# --- 适配器1: 内存存储（开发/测试用） ---
class InMemoryRepo(Repository):
    def __init__(self):
        self._data = {}
    def save(self, user):
        self._data[user["name"]] = user
        print(f"  [InMemory适配器] 存储: {user['name']}")
    def find(self, name):
        return self._data.get(name)


# --- 适配器2: 文件存储（生产环境用） ---
class FileRepo(Repository):
    """文件适配器 — 模拟持久化存储，核心代码无需任何修改"""
    def __init__(self):
        self._path = "_hex_demo_users.txt"
        if os.path.exists(self._path):
            os.remove(self._path)
    def save(self, user):
        with open(self._path, "a") as f:
            f.write(user["name"] + "\n")
        print(f"  [File适配器] 写入文件: {user['name']}")
    def find(self, name):
        try:
            with open(self._path) as f:
                names = [n.strip() for n in f]
                return {"name": name} if name in names else None
        except FileNotFoundError:
            return None


# --- 驱动适配器(Driving Adapter): 从外部调用核心 ---
def cli_adapter(service):
    """CLI驱动适配器 — 模拟用户输入调用核心，核心不知道被谁调用"""
    for name in ["Bob", "Carol", "Bob"]:
        print(f"[CLI驱动] 尝试注册: {name}")
        service.register(name)


# --- 运行演示 ---
if __name__ == "__main__":
    print("=" * 50)
    print("进阶演示：适配器替换 + 驱动适配器")
    print("=" * 50 + "\n")

    print("--- 使用内存适配器 ---")
    cli_adapter(UserService(InMemoryRepo()))
    print()

    print("--- 切换为文件适配器（核心代码零修改）---")
    service = UserService(FileRepo())
    cli_adapter(service)

    # 清理演示文件
    if os.path.exists("_hex_demo_users.txt"):
        os.remove("_hex_demo_users.txt")

    print("\n--- 与基础示例对比 ---")
    print("基础示例: 展示端口定义 + 适配器注入")
    print("进阶示例: 同一端口两个适配器自由切换 + 驱动适配器从外部调用核心")
