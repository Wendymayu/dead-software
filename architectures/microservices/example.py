"""微服务架构 (Microservices Architecture) 最小化示例

演示多个独立服务通过消息通信：
- 每个服务独立运行，有自己的数据
- 服务之间通过"网络"（此处用模拟HTTP）通信
- 每个服务可独立部署和扩展
"""

import json


# --- 模拟HTTP通信 ---
class HttpClient:
    """模拟微服务间的HTTP调用"""
    _services = {}  # 服务注册表

    @classmethod
    def register(cls, name, service):
        cls._services[name] = service
        print(f"  [网络] 服务 '{name}' 已注册")

    @classmethod
    def call(cls, service_name, method, params):
        print(f"  [HTTP] → {service_name}/{method} params={params}")
        service = cls._services.get(service_name)
        if not service:
            return {"error": "服务不存在"}
        result = service.handle(method, params)
        print(f"  [HTTP] ← {service_name} response={result}")
        return result


# --- 用户服务 ---
class UserService:
    def __init__(self):
        self._users = {"u1": {"name": "Alice", "email": "alice@example.com"}}

    def handle(self, method, params):
        if method == "get_user":
            return self._users.get(params["user_id"], {"error": "not found"})
        return {"error": "unknown method"}


# --- 订单服务 ---
class OrderService:
    def __init__(self):
        self._orders = {}

    def handle(self, method, params):
        if method == "create_order":
            # 跨服务调用：查询用户信息
            user = HttpClient.call("user-service", "get_user",
                                   {"user_id": params["user_id"]})
            if "error" in user:
                return {"error": f"用户不存在: {params['user_id']}"}
            order_id = f"o{len(self._orders) + 1}"
            self._orders[order_id] = {
                "order_id": order_id, "user": user["name"],
                "item": params["item"],
            }
            return self._orders[order_id]
        return {"error": "unknown method"}


# --- 运行演示 ---
if __name__ == "__main__":
    print("=" * 50)
    print("微服务架构演示：独立服务通过HTTP通信")
    print("=" * 50 + "\n")

    # 注册服务
    print("--- 服务注册 ---")
    HttpClient.register("user-service", UserService())
    HttpClient.register("order-service", OrderService())
    print()

    # 创建订单（订单服务会跨服务调用用户服务）
    print("--- 创建订单（跨服务调用）---")
    result = HttpClient.call("order-service", "create_order",
                             {"user_id": "u1", "item": "Python书"})
    print(f"\n最终结果: {json.dumps(result, ensure_ascii=False)}")
