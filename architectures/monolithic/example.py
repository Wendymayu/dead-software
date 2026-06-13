"""单体架构 (Monolithic Architecture) 最小化示例

演示所有功能集成在一个应用中：
- UI、业务逻辑、数据访问全部在一个类/模块中
- 简单直接，但各部分紧密耦合
- 单一部署单元，修改任何部分都需要重新部署整体
"""


class MonolithicApp:
    """单体应用：UI + 业务逻辑 + 数据访问 全在一处"""

    def __init__(self):
        # 数据直接内嵌（没有独立的数据层）
        self._users = {
            "alice": {"name": "Alice", "age": 30},
            "bob": {"name": "Bob", "age": 25},
        }
        self._orders = []

    # --- UI + 业务 + 数据混在一起 ---
    def show_user(self, user_id):
        # 直接访问内部数据，没有层级边界
        user = self._users.get(user_id)
        if user:
            print(f"[UI] 用户信息: {user['name']}, 年龄 {user['age']}")
        else:
            print(f"[UI] 用户不存在: {user_id}")

    def create_order(self, user_id, item):
        # 业务逻辑和数据访问交织在一起
        user = self._users.get(user_id)
        if not user:
            print(f"[订单] 用户不存在: {user_id}")
            return
        order = {"user": user['name'], "item": item, "status": "已创建"}
        self._orders.append(order)
        print(f"[订单] 创建成功: {user['name']} - {item}")

    def list_orders(self):
        # 直接遍历内部数据
        print(f"[UI] 订单列表:")
        for o in self._orders:
            print(f"  - {o['user']}: {o['item']} ({o['status']})")

    def update_user_age(self, user_id, new_age):
        # 直接修改内部数据
        if user_id in self._users:
            self._users[user_id]["age"] = new_age
            print(f"[用户] 已更新 {user_id} 的年龄为 {new_age}")


# --- 运行演示 ---
if __name__ == "__main__":
    app = MonolithicApp()

    print("=" * 40)
    print("单体架构演示：所有功能在一个类中")
    print("=" * 40 + "\n")

    app.show_user("alice")
    app.create_order("alice", "Python书")
    app.create_order("bob", "算法导论")
    app.update_user_age("alice", 31)
    app.show_user("alice")
    app.list_orders()
