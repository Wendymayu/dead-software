"""上帝对象 反模式 最小化示例

演示一个类包揽所有职责 vs 合理分离：
- GodObject 处理 UI、业务、数据、日志
- 分离后各类职责清晰、可独立维护
"""


# --- 反模式 ---
class GodObject:
    """一个类做所有事"""
    def show_ui(self, msg):
        print(f"[God-UI] 显示: {msg}")

    def calculate(self, a, b):
        print(f"[God-业务] 计算: {a} + {b} = {a+b}")
        return a + b

    def save_data(self, key, val):
        print(f"[God-数据] 保存: {key}={val}")

    def log(self, action):
        print(f"[God-日志] 记录: {action}")

    def run(self, a, b):
        self.log("开始运行")
        result = self.calculate(a, b)
        self.save_data("result", result)
        self.show_ui(f"结果是 {result}")
        self.log("运行完成")


# --- 正确做法 ---
class UI:
    def show(self, msg):
        print(f"[UI] 显示: {msg}")


class Calculator:
    def add(self, a, b):
        print(f"[业务] 计算: {a} + {b} = {a+b}")
        return a + b


class DataStore:
    def save(self, key, val):
        print(f"[数据] 保存: {key}={val}")


class Logger:
    def log(self, action):
        print(f"[日志] 记录: {action}")


# --- 运行演示 ---
if __name__ == "__main__":
    print("=" * 40)
    print("上帝对象 反模式演示")
    print("=" * 40 + "\n")

    print("--- 反模式: GodObject ---")
    GodObject().run(3, 5)
    print()

    print("--- 正确做法: 职责分离 ---")
    logger = Logger()
    ui = UI()
    calc = Calculator()
    store = DataStore()

    logger.log("开始运行")
    result = calc.add(3, 5)
    store.save("result", result)
    ui.show(f"结果是 {result}")
    logger.log("运行完成")

    print("\n关键：GodObject 难以维护、测试、复用")
    print("分离后各类职责清晰，可独立修改和测试")
