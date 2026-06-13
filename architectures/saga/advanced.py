"""Saga 模式进阶示例：编排式 vs 协作式

对比两种 Saga 协调风格：
- 编排式(Orchestration)：中央协调器控制流程，服务被动执行
- 协作式(Choreography)：服务自行监听事件、决定下一步动作
"""


# --- 编排式：Saga 编排器集中控制 ---
class OrchestratorSaga:
    def __init__(self, order_id):
        self.order_id = order_id
        self.compensations = []

    def run(self):
        print("  [编排器] 开始协调事务流程")
        try:
            self._step("订单创建",   "订单取消",   self.order_id)
            self._step("库存预留",   "库存释放",   self.order_id)
            self._step("支付扣款",   "支付退款",   self.order_id)
            print("  [编排器] [OK] 流程全部完成")
        except Exception as e:
            print(f"  [编排器] [FAIL] {e}，反向补偿")
            for name, args in reversed(self.compensations):
                print(f"    → {name} {args}")

    def _step(self, action, compensate, args):
        print(f"  [编排器] 执行: {action} {args}")
        self.compensations.append((compensate, args))


# --- 协作式：服务通过事件自主驱动流程 ---
class EventBus:
    def __init__(self):
        self._handlers = {}

    def on(self, event, handler):
        self._handlers.setdefault(event, []).append(handler)

    def emit(self, event, data):
        print(f"  [事件] {event}: {data}")
        for h in self._handlers.get(event, []):
            h(data)


class ChoreographyOrder:
    def __init__(self, bus):
        self.bus = bus

    def start(self, order_id):
        print(f"  [订单] 创建订单 {order_id}，发出事件")
        self.bus.emit("order_created", {"id": order_id})


class ChoreographyInventory:
    def __init__(self, bus):
        self.bus = bus
        bus.on("order_created", self.on_order)

    def on_order(self, data):
        print(f"  [库存] 预留库存，发出事件")
        self.bus.emit("inventory_reserved", data)


class ChoreographyPayment:
    def __init__(self, bus, fail=False):
        self.bus = bus
        self.fail = fail
        bus.on("inventory_reserved", self.on_reserved)

    def on_reserved(self, data):
        if self.fail:
            print(f"  [支付] [FAIL] 支付失败，发出失败事件")
            self.bus.emit("payment_failed", data)
        else:
            print(f"  [支付] 扣款成功，发出事件")
            self.bus.emit("payment_completed", data)


class ChoreographyCompensator:
    def __init__(self, bus):
        bus.on("payment_failed", self.on_failure)

    def on_failure(self, data):
        print(f"  [补偿] 收到失败事件，执行: 释放库存 → 取消订单")


if __name__ == "__main__":
    print("=" * 50)
    print("Saga 进阶：编排式 vs 协作式")
    print("=" * 50 + "\n")

    print("--- 编排式（中央协调器控制） ---")
    OrchestratorSaga("O-001").run()
    print()

    print("--- 协作式（事件驱动，服务自主） ---")
    bus = EventBus()
    ChoreographyOrder(bus)
    ChoreographyInventory(bus)
    ChoreographyPayment(bus)
    ChoreographyCompensator(bus)
    bus.on("payment_completed", lambda d: print("  [OK] 流程完成"))
    ChoreographyOrder(bus).start("C-001")
    print()

    print("--- 协作式（支付失败触发补偿） ---")
    bus2 = EventBus()
    ChoreographyOrder(bus2)
    ChoreographyInventory(bus2)
    ChoreographyPayment(bus2, fail=True)
    ChoreographyCompensator(bus2)
    ChoreographyOrder(bus2).start("C-002")
