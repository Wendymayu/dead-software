"""事件溯源进阶示例：时间旅行与业务规则演进

展示事件溯源的高级能力：
- 时间旅行：回放事件到某个时间点，重建历史状态
- 规则演进：用新业务规则重新回放旧事件，得出不同结果
"""


class EventStore:
    """事件存储，每条事件附带时间戳"""

    def __init__(self):
        self.events = []

    def append(self, event, timestamp):
        event["_ts"] = timestamp
        self.events.append(event)
        print(f"  [EventStore] 记录事件(t={timestamp}): {event['type']}")


def replay_until(events, target_time):
    """回放事件到指定时间点——时间旅行"""
    state = {"items": [], "total": 0}
    for e in events:
        if e["_ts"] > target_time:
            break
        if e["type"] == "ItemAdded":
            state["items"].append(e["item"])
            state["total"] += e["price"]
    return state


def replay_with_new_rules(events):
    """用新规则回放旧事件——业务规则演进"""
    state = {"items": [], "total": 0, "discount": 0}
    for e in events:
        if e["type"] == "ItemAdded":
            state["items"].append(e["item"])
            price = e["price"]
            # 新规则：超过200元的商品打折10%
            if price > 200:
                price = price * 0.9
                print(f"    [新规则] {e['item']} 原价{e['price']}→折后{price}")
            state["total"] += price
    return state


# --- 运行演示 ---
if __name__ == "__main__":
    es = EventStore()

    print("=" * 50)
    print("进阶演示：时间旅行 + 业务规则演进")
    print("=" * 50 + "\n")

    print("--- 记录订单事件 ---")
    es.append({"type": "ItemAdded", "item": "Python书", "price": 50}, timestamp=1)
    es.append({"type": "ItemAdded", "item": "机械键盘", "price": 300}, timestamp=2)
    es.append({"type": "ItemAdded", "item": "显示器", "price": 800}, timestamp=3)
    es.append({"type": "OrderShipped"}, timestamp=4)
    print()

    # 时间旅行：重建t=2时的状态
    print("--- 时间旅行：重建t=2时的状态 ---")
    past = replay_until(es.events, 2)
    print(f"  [t=2状态] items={past['items']}, total={past['total']}\n")

    # 旧规则回放：不打折
    print("--- 旧规则回放（不打折）---")
    old = replay_until(es.events, 999)
    print(f"  [旧规则] total={old['total']}\n")

    # 新规则回放：超过200元打折
    print("--- 新规则回放（>200元打9折）---")
    new = replay_with_new_rules(es.events)
    print(f"  [新规则] total={new['total']}\n")

    print("--- 核心洞察 ---")
    print("  同一批事件，用不同规则回放→不同结果")
    print("  这就是事件溯源的威力：事件是真相，规则是投影")
