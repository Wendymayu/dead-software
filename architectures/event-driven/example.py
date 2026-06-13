"""事件驱动架构 (Event-Driven Architecture) 最小化示例

演示事件总线 + 发布订阅模式：
- 发布者将事件发送到事件总线
- 订阅者通过事件总线接收感兴趣的事件
- 发布者和订阅者互不感知
"""


# --- 事件总线：核心中间层 ---
class EventBus:
    def __init__(self):
        self._subscribers = {}  # event_type -> [handlers]

    def subscribe(self, event_type, handler):
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(handler)
        print(f"  [EventBus] {handler.__name__} 订阅了 '{event_type}'")

    def publish(self, event_type, data):
        print(f"  [EventBus] 发布事件 '{event_type}': {data}")
        for handler in self._subscribers.get(event_type, []):
            handler(data)


# --- 订阅者：对特定事件做出响应 ---
def order_handler(data):
    print(f"    [订单服务] 处理订单: 用户={data['user']}, 商品={data['item']}")


def inventory_handler(data):
    print(f"    [库存服务] 减少库存: {data['item']}")


def notification_handler(data):
    print(f"    [通知服务] 发送通知给 {data['user']}: 您的订单已创建")


# --- 发布者：产生事件 ---
class OrderService:
    def __init__(self, bus):
        self.bus = bus

    def create_order(self, user, item):
        print(f"[OrderService] 创建订单: {user} - {item}")
        self.bus.publish("order_created", {"user": user, "item": item})


# --- 运行演示 ---
if __name__ == "__main__":
    bus = EventBus()

    print("=" * 40)
    print("事件驱动架构演示：发布者→事件总线→订阅者")
    print("=" * 40 + "\n")

    # 先订阅
    print("--- 订阅阶段 ---")
    bus.subscribe("order_created", order_handler)
    bus.subscribe("order_created", inventory_handler)
    bus.subscribe("order_created", notification_handler)
    print()

    # 再发布
    print("--- 发布阶段 ---")
    order = OrderService(bus)
    order.create_order("Alice", "Python编程书")
    print()

    # 发布无人订阅的事件
    print("--- 发布无人订阅的事件 ---")
    bus.publish("payment_processed", {"user": "Bob", "amount": 100})
