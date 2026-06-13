"""CQRS 最小化示例
写操作(Command)和读操作(Query)分离：
- CommandModel: 保证业务校验和一致性
- QueryModel: 扁平结构优化查询
- 事件总线连接两者
"""

class EventBus:
    def __init__(self):
        self._handlers = {}
    def subscribe(self, event_type, handler):
        self._handlers.setdefault(event_type, []).append(handler)
    def publish(self, event_type, data):
        for handler in self._handlers.get(event_type, []):
            handler(data)


class CommandModel:
    """写模型：关注业务规则和一致性"""
    def __init__(self, bus):
        self._products = {}
        self.bus = bus

    def create_product(self, id, name, price, stock):
        if id in self._products or price <= 0:
            print(f"  [Command] 校验失败，拒绝创建 {id}")
            return
        self._products[id] = {"name": name, "price": price, "stock": stock}
        print(f"  [Command] 创建产品: {name}, 价格={price}, 库存={stock}")
        self.bus.publish("product_created", {"name": name, "price": price, "stock": stock})

    def update_stock(self, id, delta):
        p = self._products.get(id)
        if not p or p["stock"] + delta < 0:
            print(f"  [Command] 库存不足或不存在，拒绝 {id}")
            return
        p["stock"] += delta
        print(f"  [Command] 更新库存: {id} → {p['stock']}")
        self.bus.publish("stock_updated", {"name": p["name"], "stock": p["stock"]})


class QueryModel:
    """读模型：按名称索引，优化搜索"""
    def __init__(self):
        self._catalog = {}

    def on_product_created(self, data):
        self._catalog[data["name"]] = {"price": data["price"], "stock": data["stock"]}
        print(f"  [Query] 目录更新: {data['name']}")

    def on_stock_updated(self, data):
        self._catalog[data["name"]]["stock"] = data["stock"]
        print(f"  [Query] 库存同步: {data['name']} → {data['stock']}")

    def search(self, keyword):
        results = {k: v for k, v in self._catalog.items() if keyword in k}
        print(f"  [Query] 搜索 '{keyword}' → {results}")


if __name__ == "__main__":
    bus = EventBus()
    write = CommandModel(bus)
    read = QueryModel()
    bus.subscribe("product_created", read.on_product_created)
    bus.subscribe("stock_updated", read.on_stock_updated)

    print("=" * 40)
    print("CQRS演示：写模型保证一致性，读模型优化查询")
    print("=" * 40 + "\n")
    print("--- 创建产品(写操作) ---")
    write.create_product("p1", "Python入门", 59, 100)
    write.create_product("p2", "算法导论", 128, 50)
    print("\n--- 校验失败 ---")
    write.create_product("p1", "重复", 59, 100)
    write.create_product("p3", "空书", -1, 10)
    print("\n--- 查询产品(读操作) ---")
    read.search("Python")
    read.search("算法")
