"""CQRS 进阶示例：事件溯源 + 读模型重建

展示两个关键能力：
- 事件溯源：所有状态变更记录为事件，可从事件重建写模型
- 读模型重建：从事件流重新生成读模型，读模型可以是与写模型完全不同的结构
"""


# --- 事件存储：所有变更的历史记录 ---
class EventStore:
    def __init__(self):
        self._events = []  # append-only 事件日志

    def append(self, event_type, data):
        self._events.append({"type": event_type, "data": data})
        print(f"  [EventStore] 记录事件: {event_type}")

    def replay(self):
        print("  [EventStore] 重放所有事件:")
        for e in self._events:
            print(f"    → {e['type']}: {e['data']}")
        return list(self._events)


# --- 写模型：通过事件溯源重建状态 ---
class CommandModel:
    def __init__(self, event_store):
        self.event_store = event_store
        self._products = {}  # 从事件重建的当前状态

    def rebuild_from_events(self):
        """从事件流重建写模型状态"""
        self._products = {}
        for event in self.event_store.replay():
            if event["type"] == "product_created":
                d = event["data"]
                self._products[d["id"]] = {"name": d["name"], "price": d["price"], "stock": d["stock"]}
            elif event["type"] == "stock_updated":
                self._products[event["data"]["id"]]["stock"] = event["data"]["stock"]
        print(f"  [Command] 重建完成，当前状态: {self._products}")

    def create_product(self, id, name, price, stock):
        if price <= 0:
            print(f"  [Command] 价格无效，拒绝")
            return None
        self.event_store.append("product_created", {"id": id, "name": name, "price": price, "stock": stock})
        self._products[id] = {"name": name, "price": price, "stock": stock}
        return id

    def update_stock(self, id, delta):
        product = self._products.get(id)
        if not product or product["stock"] + delta < 0:
            print(f"  [Command] 库存不足或产品不存在，拒绝")
            return None
        new_stock = product["stock"] + delta
        self.event_store.append("stock_updated", {"id": id, "stock": new_stock})
        product["stock"] = new_stock
        return id


# --- 读模型：与写模型不同的扁平结构 ---
class QueryModel:
    """读模型结构可以完全不同于写模型——此处为面向查询的扁平列表"""

    def __init__(self):
        self._flat_list = []  # 扁平视图：[{name, price, stock, label}]

    def rebuild_from_events(self, events):
        """从事件流重建读模型——结构与写模型不同"""
        self._flat_list = []
        products = {}
        for event in events:
            if event["type"] == "product_created":
                d = event["data"]
                products[d["id"]] = d.copy()
            elif event["type"] == "stock_updated":
                products[event["data"]["id"]]["stock"] = event["data"]["stock"]
        # 扁平化为查询友好的结构（写模型是dict，读模型是list+label）
        for p in products.values():
            label = "热销" if p["stock"] > 80 else "正常" if p["stock"] > 20 else "低库存"
            self._flat_list.append({"name": p["name"], "price": p["price"], "stock": p["stock"], "label": label})
        print(f"  [Query] 读模型重建完成(扁平列表): {self._flat_list}")

    def list_products(self):
        for item in self._flat_list:
            print(f"    {item['name']} | {item['price']}元 | 库存:{item['stock']} | {item['label']}")


# --- 运行演示 ---
if __name__ == "__main__":
    store = EventStore()
    write = CommandModel(store)
    read = QueryModel()

    print("=" * 50)
    print("进阶演示：事件溯源 + 读模型重建（不同结构）")
    print("=" * 50 + "\n")

    print("--- 写操作产生事件 ---")
    write.create_product("p1", "Python入门", 59, 100)
    write.create_product("p2", "算法导论", 128, 50)
    write.update_stock("p1", -20)  # 卖出20本
    write.update_stock("p2", -40)  # 卖出40本
    print()

    print("--- 从事件重建读模型(扁平结构) ---")
    read.rebuild_from_events(store.replay())
    read.list_products()
    print()

    print("--- 模拟读模型损坏，从事件重建 ---")
    read2 = QueryModel()
    print("  [场景] 读模型数据丢失，需要重建")
    read2.rebuild_from_events(store.replay())
    read2.list_products()
