"""事件溯源 (Event Sourcing) 最小化示例

演示事件溯源的核心机制：
- 不存储当前状态，而是存储导致状态变化的事件序列
- 通过回放事件序列重建当前状态
- 与传统"直接存储状态"方式对比
"""


# --- 事件溯源：存储事件而非状态 ---
class EventStore:
    """事件存储——只记录事件，不保存状态"""

    def __init__(self):
        self.events = []

    def append(self, event):
        self.events.append(event)
        print(f"  [EventStore] 记录事件: {event}")


def replay(events):
    """回放事件序列，推导出当前状态"""
    state = {"items": [], "status": "created"}
    for e in events:
        kind = e["type"]
        if kind == "OrderCreated":
            state["user"] = e["user"]
        elif kind == "ItemAdded":
            state["items"].append(e["item"])
        elif kind == "OrderShipped":
            state["status"] = "shipped"
    return state


# --- 传统方式：直接存储当前状态 ---
class StateStore:
    """传统方式——每次变化直接覆盖状态"""

    def __init__(self):
        self.state = {}

    def save(self, state):
        self.state = state
        print(f"  [StateStore] 保存状态: {state}")


# --- 运行演示 ---
if __name__ == "__main__":
    es = EventStore()
    ss = StateStore()

    print("=" * 40)
    print("事件溯源演示：存储事件 vs 存储状态")
    print("=" * 40 + "\n")

    # 事件溯源方式
    print("--- 事件溯源：记录事件 ---")
    es.append({"type": "OrderCreated", "user": "Alice"})
    es.append({"type": "ItemAdded", "item": "Python书"})
    es.append({"type": "ItemAdded", "item": "键盘"})
    es.append({"type": "OrderShipped"})
    print()

    order = replay(es.events)
    print(f"  [回放结果] 当前状态: {order}\n")

    # 传统方式
    print("--- 传统方式：直接覆盖状态 ---")
    ss.save({"user": "Alice", "items": [], "status": "created"})
    ss.save({"user": "Alice", "items": ["Python书"], "status": "created"})
    ss.save({"user": "Alice", "items": ["Python书", "键盘"], "status": "created"})
    ss.save({"user": "Alice", "items": ["Python书", "键盘"], "status": "shipped"})
    print()

    print("--- 事件溯源 vs 传统 ---")
    print("  事件溯源: 保留了4条事件，可回溯任意历史")
    print("  传统方式: 只保留最终状态，历史丢失")
