"""Actor 进阶示例：ActorSystem + 多类型 Actor 协作

展示 Actor 模型的进阶能力：
- ActorSystem 管理所有 Actor 的生命周期和消息调度
- 多种 Actor 类型协作完成复杂任务
- Actor 可创建新 Actor（动态扩展系统）
"""


class Actor:
    def __init__(self, name, system):
        self._name = name
        self._system = system
        self._mailbox = []
        self._state = {}

    def send(self, target_name, message):
        """通过系统路由发送——Actor 不直接持有其他 Actor 引用"""
        print(f"  [{self._name}] → {target_name}: {message['type']}")
        self._system.deliver(target_name, (self._name, message))

    def receive(self, sender_name, message):
        """处理一条消息"""
        pass

    def process_all(self):
        while self._mailbox:
            sender_name, message = self._mailbox.pop(0)
            self.receive(sender_name, message)


class ActorSystem:
    """管理所有 Actor，统一调度消息传递"""
    def __init__(self):
        self._actors = {}

    def create(self, actor_class, name):
        actor = actor_class(name, self)
        self._actors[name] = actor
        print(f"[System] 创建 Actor: {name}")
        return actor

    def deliver(self, target_name, envelope):
        target = self._actors.get(target_name)
        if target:
            target._mailbox.append(envelope)
        else:
            print(f"  [System] Actor {target_name} 不存在")

    def run_all(self):
        """让所有 Actor 处理各自邮箱中的消息"""
        for actor in self._actors.values():
            actor.process_all()


# --- 具体 Actor ---
class OrderActor(Actor):
    def receive(self, sender, msg):
        if msg["type"] == "PLACE_ORDER":
            self._state["order_id"] = msg["order_id"]
            print(f"  [OrderActor] 处理订单: {msg['order_id']}")
            # 订单需要库存检查 → 向 InventoryActor 发消息
            self.send("inventory", {"type": "CHECK_STOCK", "item": msg["item"]})


class InventoryActor(Actor):
    def receive(self, sender, msg):
        if msg["type"] == "CHECK_STOCK":
            in_stock = True  # 简化：总是有库存
            print(f"  [InventoryActor] 库存检查: {msg['item']} → 有库存")
            # 库存确认后 → 通知 PaymentActor
            self.send("payment", {"type": "CHARGE", "order_id": sender, "amount": 100})


class PaymentActor(Actor):
    def receive(self, sender, msg):
        if msg["type"] == "CHARGE":
            print(f"  [PaymentActor] 扣款: 订单 {msg['order_id']}, 金额 {msg['amount']}")
            # 支付完成 → 通知 OrderActor
            self.send("order", {"type": "PAYMENT_DONE", "order_id": msg["order_id"]})


# --- 运行演示 ---
if __name__ == "__main__":
    system = ActorSystem()
    system.create(OrderActor, "order")
    system.create(InventoryActor, "inventory")
    system.create(PaymentActor, "payment")

    print("=" * 50)
    print("进阶演示: ActorSystem + 多 Actor 协作完成订单")
    print("=" * 50 + "\n")

    # 客户发送下单消息给 OrderActor
    system.deliver("order", ("client", {"type": "PLACE_ORDER", "order_id": "ORD-1", "item": "book"}))

    # 系统调度：每轮所有 Actor 处理消息，直到全部邮箱清空
    for i in range(4):
        print(f"\n--- 第 {i+1} 轮消息处理 ---")
        system.run_all()
