"""绞杀者模式 (Strangler Fig Pattern) 最小化示例
演示渐进式系统替换：
- 旧系统与新系统并存
- 路由层（绞杀者）决定谁处理请求
- 逐步将功能从旧系统迁移到新系统
"""

# --- 旧系统（遗留）---
class LegacySystem:
    """遗留系统：处理所有业务请求"""
    def get_user(self, user_id):
        print(f"  [旧系统] 查询用户 {user_id}（慢查询）")
        return {"id": user_id, "name": "Alice", "source": "legacy"}

    def get_order(self, order_id):
        print(f"  [旧系统] 查询订单 {order_id}（慢查询）")
        return {"id": order_id, "item": "Book", "source": "legacy"}

    def get_product(self, product_id):
        print(f"  [旧系统] 查询商品 {product_id}（慢查询）")
        return {"id": product_id, "name": "Python Guide", "source": "legacy"}

# --- 新系统 ---
class NewSystem:
    """新系统：更快、更好的实现"""
    def get_user(self, user_id):
        print(f"  [新系统] 查询用户 {user_id}（快速查询）")
        return {"id": user_id, "name": "Alice", "source": "new"}

    def get_product(self, product_id):
        print(f"  [新系统] 查询商品 {product_id}（快速查询）")
        return {"id": product_id, "name": "Python Guide", "source": "new"}

# --- 绞杀者路由层 ---
class StranglerRouter:
    """路由层：决定请求由旧系统还是新系统处理"""
    def __init__(self, legacy, new):
        self._legacy = legacy
        self._new = new
        self._routes = {}  # method -> "legacy" or "new"

    def add_route(self, method, target):
        """将某个方法的路由指向新系统"""
        self._routes[method] = target
        print(f"[路由] '{method}' → {target}")

    def handle(self, method, *args):
        target = self._routes.get(method, "legacy")
        system = self._new if target == "new" else self._legacy
        return getattr(system, method)(*args)

# --- 运行演示 ---
if __name__ == "__main__":
    print("=" * 40)
    print("绞杀者模式演示：渐进式系统迁移")
    print("=" * 40 + "\n")

    legacy = LegacySystem()
    new = NewSystem()
    router = StranglerRouter(legacy, new)

    # 阶段1：所有请求走旧系统
    print("--- 阶段1: 100%旧系统 ---")
    router.handle("get_user", "u1")
    router.handle("get_order", "o1")
    router.handle("get_product", "p1")
    print()

    # 阶段2：逐步迁移用户查询
    print("--- 阶段2: 迁移用户查询到新系统 ---")
    router.add_route("get_user", "new")
    router.handle("get_user", "u1")   # → 新系统
    router.handle("get_order", "o1")   # → 仍走旧系统
    print()

    # 阶段3：继续迁移商品查询
    print("--- 阶段3: 迁移商品查询到新系统 ---")
    router.add_route("get_product", "new")
    router.handle("get_user", "u1")    # → 新系统
    router.handle("get_product", "p1")  # → 新系统
