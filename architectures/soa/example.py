"""SOA (Service-Oriented Architecture) 最小化示例

模拟服务通过 ESB 通信：各服务独立部署，通过标准契约交互。
ESB 负责路由、转换、协调——这是 SOA 与微服务的关键区别。
"""


# --- ESB：服务总线，路由和协调所有服务间通信 ---
class ESB:
    def __init__(self):
        self._services = {}

    def register(self, name, service):
        self._services[name] = service
        print(f"[ESB] 注册服务: {name}")

    def call(self, target, action, params):
        """所有服务间通信必须通过 ESB，ESB 负责路由"""
        print(f"  [ESB] 转发请求 → {target}: {action}")
        service = self._services.get(target)
        if not service:
            return {"status": "ERROR", "msg": f"服务 {target} 未注册"}
        return service.handle(action, params)


# --- 服务：各自独立，通过标准接口与 ESB 交互 ---
class UserService:
    def handle(self, action, params):
        print(f"    [UserService] 处理: {action}")
        if action == "GET_USER":
            return {"status": "OK", "data": {"name": params["name"], "age": 30}}
        return {"status": "ERROR", "msg": "不支持的操作"}


class OrderService:
    def handle(self, action, params):
        print(f"    [OrderService] 处理: {action}")
        if action == "CREATE_ORDER":
            return {"status": "OK", "order_id": "ORD-001", "total": 99.9}
        return {"status": "ERROR", "msg": "不支持的操作"}


class PaymentService:
    def handle(self, action, params):
        print(f"    [PaymentService] 处理: {action}")
        if action == "PAY":
            return {"status": "OK", "txn_id": "TXN-001"}
        return {"status": "ERROR", "msg": "不支持的操作"}


# --- 运行演示 ---
if __name__ == "__main__":
    esb = ESB()
    esb.register("user", UserService())
    esb.register("order", OrderService())
    esb.register("payment", PaymentService())

    print("=" * 45)
    print("SOA 演示: 所有服务通过 ESB 通信")
    print("=" * 45 + "\n")

    # 业务流程：查用户 → 下单 → 支付，全部通过 ESB 路由
    r1 = esb.call("user", "GET_USER", {"name": "Alice"})
    print(f"  → 响应: {r1}\n")

    r2 = esb.call("order", "CREATE_ORDER", {"user": "Alice"})
    print(f"  → 响应: {r2}\n")

    r3 = esb.call("payment", "PAY", {"order_id": "ORD-001"})
    print(f"  → 响应: {r3}")
