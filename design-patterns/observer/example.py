"""观察者模式 (Observer Pattern) 最小化示例

演示一对多的依赖关系：
- 被观察者(Subject)状态变化时，自动通知所有观察者
- 观察者无需主动查询，被动接收通知
"""


class Subject:
    """被观察者：维护观察者列表并通知变化"""

    def __init__(self):
        self._observers = []
        self._state = None

    def attach(self, observer):
        self._observers.append(observer)
        print(f"  [Subject] 添加观察者: {observer.__class__.__name__}")

    def detach(self, observer):
        self._observers.remove(observer)

    def notify(self):
        print(f"  [Subject] 通知所有观察者: state={self._state}")
        for observer in self._observers:
            observer.update(self._state)

    def set_state(self, state):
        self._state = state
        print(f"[Subject] 状态变更: {state}")
        self.notify()


class EmailNotifier:
    def update(self, state):
        print(f"    [EmailNotifier] 发送邮件: 温度变为 {state}C")


class Logger:
    def update(self, state):
        print(f"    [Logger] 记录日志: temperature={state}")


class AlertSystem:
    def update(self, state):
        if state > 35:
            print(f"    [AlertSystem] [WARNING] 高温警报: {state}C!")
        else:
            print(f"    [AlertSystem] 温度正常: {state}C")


# --- 运行演示 ---
if __name__ == "__main__":
    print("=" * 40)
    print("观察者模式演示：状态变化→自动通知所有观察者")
    print("=" * 40 + "\n")

    sensor = Subject()
    sensor.attach(EmailNotifier())
    sensor.attach(Logger())
    sensor.attach(AlertSystem())

    print("--- 温度变更 ---\n")
    sensor.set_state(25)
    print()
    sensor.set_state(38)
