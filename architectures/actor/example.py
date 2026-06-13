"""Actor 架构 (Actor Model) 最小化示例

每个 Actor 有独立状态 + 邙箱，只通过异步消息通信，无共享状态。
展示 CounterActor 和 PrinterActor 互相发送消息。
"""


# --- Actor：独立状态 + 邙箱 + 异步消息 ---
class Actor:
    def __init__(self, name):
        self._name = name
        self._mailbox = []  # 消息队列（邮箱）
        self._state = {}    # 私有状态，其他 Actor 无法直接访问

    def send(self, target, message):
        """向目标 Actor 发送消息——唯一的通信方式"""
        print(f"  [{self._name}] 发送消息给 {target._name}: {message}")
        target._mailbox.append((self, message))

    def process_messages(self):
        """处理邮箱中的所有消息"""
        while self._mailbox:
            sender, message = self._mailbox.pop(0)
            self._on_receive(sender, message)

    def _on_receive(self, sender, message):
        """子类重写此方法来处理具体消息"""
        raise NotImplementedError


# --- CounterActor：维护计数状态 ---
class CounterActor(Actor):
    def __init__(self, name):
        super().__init__(name)
        self._state["count"] = 0

    def _on_receive(self, sender, message):
        if message["type"] == "INCREMENT":
            self._state["count"] += 1
            print(f"  [{self._name}] 计数增加 → {self._state['count']}")
            # 计数变化后通知 PrinterActor
            self.send(sender, {"type": "COUNT_UPDATE", "count": self._state["count"]})
        elif message["type"] == "GET_COUNT":
            self.send(sender, {"type": "COUNT_RESPONSE", "count": self._state["count"]})


# --- PrinterActor：接收消息并打印 ---
class PrinterActor(Actor):
    def __init__(self, name):
        super().__init__(name)

    def _on_receive(self, sender, message):
        if message["type"] == "COUNT_UPDATE":
            print(f"  [{self._name}] 收到计数更新: {message['count']}")
        elif message["type"] == "COUNT_RESPONSE":
            print(f"  [{self._name}] 查询到当前计数: {message['count']}")


# --- 运行演示 ---
if __name__ == "__main__":
    counter = CounterActor("counter")
    printer = PrinterActor("printer")

    print("=" * 40)
    print("Actor 演示: 异步消息通信，无共享状态")
    print("=" * 40 + "\n")

    # Printer 发送 INCREMENT 消息给 Counter
    printer.send(counter, {"type": "INCREMENT"})
    counter.process_messages()  # Counter 处理消息并回发
    printer.process_messages()  # Printer 处理回复

    print()
    printer.send(counter, {"type": "INCREMENT"})
    counter.process_messages()
    printer.process_messages()

    print()
    printer.send(counter, {"type": "GET_COUNT"})
    counter.process_messages()
    printer.process_messages()
