"""单体架构进阶示例：模块化单体 (Modular Monolith)

展示单体架构的最佳实践：
- 仍然是一个部署单元
- 但内部按模块划分边界，每个模块有自己的数据和接口
- 模块间通过明确接口通信，不直接访问彼此数据
- 为未来拆分为微服务做准备
"""


class UserModule:
    """用户模块：封装用户相关所有逻辑和数据"""

    def __init__(self):
        self._users = {"alice": {"name": "Alice", "age": 30}}

    def get_user(self, user_id):
        """公开接口：只返回必要信息，不暴露内部数据结构"""
        user = self._users.get(user_id)
        if user:
            return {"name": user["name"], "age": user["age"]}
        return None

    def update_age(self, user_id, new_age):
        if user_id in self._users:
            self._users[user_id]["age"] = new_age
            return True
        return False


class OrderModule:
    """订单模块：只依赖 UserModule 的公开接口，不直接访问其数据"""

    def __init__(self, user_module):
        self.user_module = user_module  # 通过接口依赖，不是数据依赖
        self._orders = []

    def create_order(self, user_id, item):
        user = self.user_module.get_user(user_id)  # 只用公开接口
        if not user:
            print(f"  [OrderModule] 用户不存在: {user_id}")
            return None
        order = {"user_name": user["name"], "item": item}
        self._orders.append(order)
        print(f"  [OrderModule] 订单创建: {user['name']} - {item}")
        return order

    def list_orders(self):
        return self._orders


class ModularMonolithApp:
    """模块化单体：统一部署，但内部有清晰模块边界"""

    def __init__(self):
        self.users = UserModule()
        self.orders = OrderModule(self.users)  # 模块间通过接口连接

    def show_user(self, user_id):
        user = self.users.get_user(user_id)
        if user:
            print(f"[App] 用户: {user['name']}, 年龄 {user['age']}")
        else:
            print(f"[App] 用户不存在: {user_id}")

    def create_order(self, user_id, item):
        self.orders.create_order(user_id, item)

    def list_orders(self):
        print("[App] 订单列表:")
        for o in self.orders.list_orders():
            print(f"  - {o['user_name']}: {o['item']}")


# --- 运行演示 ---
if __name__ == "__main__":
    app = ModularMonolithApp()

    print("=" * 50)
    print("进阶演示：模块化单体 — 单一部署 + 内部模块边界")
    print("=" * 50 + "\n")

    app.show_user("alice")
    app.create_order("alice", "Python书")
    app.create_order("unknown", "不存在")  # 模块边界保护
    app.list_orders()

    print("\n--- 与基础单体对比 ---")
    print("基础单体: 所有代码在一个类，直接访问内部数据")
    print("模块化单体: 模块间通过接口通信，不直接访问彼此数据")
    print("         未来拆分微服务时，每个模块可独立抽出")
