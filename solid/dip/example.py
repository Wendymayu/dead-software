"""依赖倒置原则 (DIP) 最小化示例

演示高层模块依赖低层具体类 vs 依赖抽象接口：
- BadBusiness 直接依赖 MySQLRepo 具体实现
- GoodBusiness 依赖抽象 DataRepo 接口
- 切换数据实现时无需修改业务逻辑
"""

from abc import ABC, abstractmethod


# --- 违反 DIP ---
class MySQLRepo:
    """低层模块：具体数据存储"""
    def fetch(self, key):
        print(f"[MySQL] 从MySQL获取: {key}")
        return f"mysql_data({key})"


class BadBusiness:
    """高层模块直接依赖具体实现"""
    def __init__(self):
        self._repo = MySQLRepo()  # 紧耦合！

    def get_data(self, key):
        return self._repo.fetch(key)


# --- 遵循 DIP ---
class DataRepo(ABC):
    """抽象接口：高层和低层都依赖此抽象"""
    @abstractmethod
    def fetch(self, key): ...


class RedisRepo(DataRepo):
    def fetch(self, key):
        print(f"[Redis] 从Redis获取: {key}")
        return f"redis_data({key})"


class MockRepo(DataRepo):
    def fetch(self, key):
        print(f"[Mock] 从Mock获取: {key}")
        return f"mock_data({key})"


class GoodBusiness:
    """高层模块依赖抽象，通过注入切换实现"""
    def __init__(self, repo: DataRepo):
        self._repo = repo  # 依赖抽象！

    def get_data(self, key):
        return self._repo.fetch(key)


# --- 运行演示 ---
if __name__ == "__main__":
    print("=" * 40)
    print("DIP 演示：依赖倒置原则")
    print("=" * 40 + "\n")

    print("--- 违反 DIP ---")
    bad = BadBusiness()
    print(f"  结果: {bad.get_data('user_1')}")
    print()

    print("--- 遵循 DIP ---")
    for repo in [RedisRepo(), MockRepo()]:
        biz = GoodBusiness(repo)
        print(f"  结果: {biz.get_data('user_1')}")
    print()

    print("关键区别：BadBusiness 换数据源必须改代码")
    print("GoodBusiness 通过注入切换，业务逻辑不变")
