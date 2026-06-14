"""CQRS 进阶示例：模拟 Axon Framework 命令查询职责分离

展示 Axon CQRS+ES 核心机制：
- CommandBus: 分发命令到 CommandHandler（写端）
- QueryBus: 分发查询到 QueryHandler（读端）
- EventStore: 事件持久化（append-only）
- Projection: 从事件流构建读模型
- 流程: CreateOrder → 事件存储 → 查询订单 → 读投影
"""

from datetime import datetime


class EventStore:
    """Axon EventStore: 事件持久化"""
    def __init__(self):
        self._streams = {}

    def append(self, agg_id, event_type, data):
        self._streams.setdefault(agg_id, []).append(
            {"type": event_type, "data": data, "ts": datetime.now().isoformat()})
        print(f"  [EventStore] append → {agg_id}/{event_type}")

    def all_events(self):
        ev = [e for s in self._streams.values() for e in s]
        print(f"  [EventStore] all → {len(ev)} 事件")
        return ev


class Bus:
    """Axon CommandBus/QueryBus: 分发命令或查询"""
    def __init__(self, label):
        self._handlers, self.label = {}, label

    def register(self, type_, handler):
        self._handlers[type_] = handler

    def dispatch(self, type_, payload=None):
        print(f"[{self.label}] dispatch({type_})")
        return self._handlers[type_].handle(payload or {})


class OrderCommandHandler:
    """CommandHandler: 验证命令 → 生成事件"""
    def __init__(self, store):
        self.store = store

    def handle(self, payload):
        cmd = payload.get("cmd", "create")
        if cmd == "create":
            print(f"[CommandHandler] CreateOrder(id={payload['id']}, product={payload['product']})")
            self.store.append(payload["id"], "OrderCreated",
                              {"id": payload["id"], "product": payload["product"]})
        elif cmd == "cancel":
            print(f"[CommandHandler] CancelOrder(id={payload['id']})")
            self.store.append(payload["id"], "OrderCancelled", {"id": payload["id"]})


class OrderProjection:
    """Projection: 从事件流构建读模型"""
    def __init__(self):
        self._view = {}

    def rebuild(self, events):
        print("[Projection] 从事件重建读模型...")
        self._view = {}
        for e in events:
            d = e["data"]
            if e["type"] == "OrderCreated":
                self._view[d["id"]] = {"product": d["product"], "status": "已创建"}
            elif e["type"] == "OrderCancelled":
                self._view[d["id"]]["status"] = "已取消"
        print(f"  [Projection] 重建完成 → {len(self._view)} 条")

    def handle(self, payload):
        print("[QueryHandler] QueryOrderList()")
        for oid, info in self._view.items():
            print(f"  → 订单#{oid}: {info['product']} | {info['status']}")

if __name__ == "__main__":
    store = EventStore()
    cmd_bus, qry_bus = Bus("CommandBus"), Bus("QueryBus")
    cmd_bus.register("order", OrderCommandHandler(store))
    proj = OrderProjection()
    qry_bus.register("order_list", proj)

    print("=" * 50)
    print("Axon Framework CQRS 模拟")
    print("=" * 50 + "\n")

    print("--- 命令端: 创建/取消订单 → 事件存储 ---")
    cmd_bus.dispatch("order", {"cmd": "create", "id": "O1", "product": "笔记本电脑"})
    cmd_bus.dispatch("order", {"cmd": "create", "id": "O2", "product": "键盘"})
    cmd_bus.dispatch("order", {"cmd": "cancel", "id": "O2"})

    print("\n--- 查询端: 重建投影 → 查询订单 ---")
    proj.rebuild(store.all_events())
    qry_bus.dispatch("order_list")
