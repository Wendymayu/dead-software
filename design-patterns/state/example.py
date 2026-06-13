"""状态模式 (State Pattern) 最小化示例

演示对象行为随内部状态变化而变化：
- 每个状态封装为一个类，处理该状态下的允许操作
- 消除大量 if/else 状态判断
- 状态转换由状态类自身决定
"""


class OrderState:
    """状态基类：定义各操作在该状态下的行为"""

    def pay(self, order): ...
    def ship(self, order): ...
    def deliver(self, order): ...


class Created(OrderState):
    """已创建：只能付款"""

    def pay(self, order):
        print(f"  [Created→Paid] 订单 {order._id} 付款成功")
        order._state = Paid()

    def ship(self, order):
        print("  [Created] [X] 未付款，无法发货")

    def deliver(self, order):
        print("  [Created] [X] 未付款未发货，无法签收")


class Paid(OrderState):
    """已付款：可以发货"""

    def pay(self, order):
        print("  [Paid] [X] 已付款，无需重复付款")

    def ship(self, order):
        print(f"  [Paid→Shipped] 订单 {order._id} 已发货")
        order._state = Shipped()

    def deliver(self, order):
        print("  [Paid] [X] 未发货，无法签收")


class Shipped(OrderState):
    """已发货：可以签收"""

    def pay(self, order):
        print("  [Shipped] [X] 已付款，无需重复")

    def ship(self, order):
        print("  [Shipped] [X] 已发货，无需重复发货")

    def deliver(self, order):
        print(f"  [Shipped→Delivered] 订单 {order._id} 已签收")
        order._state = Delivered()


class Delivered(OrderState):
    """已签收：所有操作已完成"""

    def pay(self, order):
        print("  [Delivered] [X] 流程已结束")

    def ship(self, order):
        print("  [Delivered] [X] 流程已结束")

    def deliver(self, order):
        print("  [Delivered] [X] 已签收，无需重复")


class Order:
    """上下文：持有当前状态，委托操作给状态对象"""

    def __init__(self, id):
        self._id = id
        self._state = Created()

    def pay(self):
        print(f"[Order {self._id}] 尝试付款 (状态: {self._state.__class__.__name__})")
        self._state.pay(self)

    def ship(self):
        print(f"[Order {self._id}] 尝试发货 (状态: {self._state.__class__.__name__})")
        self._state.ship(self)

    def deliver(self):
        print(f"[Order {self._id}] 尝试签收 (状态: {self._state.__class__.__name__})")
        self._state.deliver(self)


# --- 运行演示 ---
if __name__ == "__main__":
    print("=" * 40)
    print("状态模式演示：订单状态流转与行为变化")
    print("=" * 40 + "\n")

    order = Order("20240001")

    order.ship()  # 未付款不能发货
    order.pay()   # 付款 → Created→Paid
    order.pay()   # 已付款不能重复付
    order.ship()  # 发货 → Paid→Shipped
    order.deliver()  # 签收 → Shipped→Delivered
