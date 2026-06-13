"""接口隔离原则 (ISP) 最小化示例

演示胖接口 vs 精简接口：
- FatInterface 强迫所有客户端实现不需要的方法
- 精简接口让每个客户端只实现自己用到的方法
"""
from abc import ABC, abstractmethod

# --- 违反 ISP ---
class FatWorker(ABC):
    """胖接口：所有客户端被迫实现全部方法"""
    @abstractmethod
    def work(self): ...
    @abstractmethod
    def eat(self): ...

class HumanWorker(FatWorker):
    def work(self):
        print("[Human] 工作")
    def eat(self):
        print("[Human] 吃饭")

class RobotWorker(FatWorker):
    """机器人：被迫实现 eat()，但机器人不吃饭！"""
    def work(self):
        print("[Robot] 工作")
    def eat(self):
        raise NotImplementedError("机器人不需要吃饭！")

# --- 遵循 ISP ---
class Workable(ABC):
    @abstractmethod
    def work(self): ...

class Eatable(ABC):
    @abstractmethod
    def eat(self): ...

class GoodHuman(Workable, Eatable):
    def work(self):
        print("[GoodHuman] 工作")
    def eat(self):
        print("[GoodHuman] 吃饭")

class GoodRobot(Workable):
    """只实现 Workable，无需实现 eat"""
    def work(self):
        print("[GoodRobot] 工作")

# --- 运行演示 ---
if __name__ == "__main__":
    print("=" * 40)
    print("ISP 演示：接口隔离原则")
    print("=" * 40 + "\n")

    print("--- 违反 ISP (胖接口) ---")
    HumanWorker().work()
    HumanWorker().eat()
    RobotWorker().work()
    try:
        RobotWorker().eat()
    except NotImplementedError as e:
        print(f"[Robot] {e}")
    print()

    print("--- 遵循 ISP (精简接口) ---")
    GoodHuman().work()
    GoodHuman().eat()
    GoodRobot().work()
    print()

    print("关键区别：RobotWorker 被迫实现不需要的 eat()")
    print("GoodRobot 只实现 Workable，接口干净")
