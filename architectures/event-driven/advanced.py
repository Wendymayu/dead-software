"""事件驱动架构进阶示例：事件过滤与链式处理

展示事件驱动的更复杂场景：
- 事件过滤：订阅者可以只接收符合条件的事件
- 链式处理：一个事件的处理结果可以触发新事件
"""


class EventBus:
    def __init__(self):
        self._subscribers = {}

    def subscribe(self, event_type, handler, filter_fn=None):
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append((handler, filter_fn))

    def publish(self, event_type, data):
        print(f"  [EventBus] 事件 '{event_type}': {data}")
        for handler, filter_fn in self._subscribers.get(event_type, []):
            if filter_fn is None or filter_fn(data):
                handler(data)


# --- 事件处理链 ---
def validate_order(data):
    if data.get("amount", 0) > 0:
        print(f"    [验证] 订单有效: {data['user']}, 金额={data['amount']}")
    else:
        print(f"    [验证] 订单无效: 金额为0")


def on_order_valid(data):
    print(f"    [处理] 执行订单: {data['user']}")


# --- 过滤函数：只处理大额订单 ---
def is_large_order(data):
    return data.get("amount", 0) >= 100


def vip_handler(data):
    print(f"    [VIP处理] 大额订单特殊处理: {data['user']}, 金额={data['amount']}")


# --- 运行演示 ---
if __name__ == "__main__":
    bus = EventBus()

    print("=" * 50)
    print("进阶演示：事件过滤 + 链式处理")
    print("=" * 50 + "\n")

    bus.subscribe("order_created", validate_order)
    bus.subscribe("order_created", on_order_valid)
    bus.subscribe("order_created", vip_handler, filter_fn=is_large_order)

    print("--- 小额订单 ---")
    bus.publish("order_created", {"user": "Alice", "amount": 50})
    print()

    print("--- 大额订单（触发VIP处理）---")
    bus.publish("order_created", {"user": "Bob", "amount": 200})
