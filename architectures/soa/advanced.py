"""SOA 进阶示例：ESB 消息转换 + 服务编排

展示 SOA 的核心能力：
- ESB 做消息格式转换——服务不需要了解其他服务的内部格式
- ESB 编排业务流程——跨服务的复合操作由 ESB 协调
- 服务治理——统一日志、错误处理、重试策略
"""


# --- ESB：消息转换 + 编排 + 治理 ---
class ESB:
    def __init__(self):
        self._services = {}
        self._logs = []

    def register(self, name, service):
        self._services[name] = service

    def call(self, target, action, params):
        self._logs.append(f"调用 {target}.{action}")
        service = self._services.get(target)
        if not service:
            return {"status": "ERROR", "msg": f"服务 {target} 未注册"}
        return service.handle(action, params)

    def orchestrate(self, flow_name, params):
        """ESB 编排跨服务业务流程"""
        print(f"[ESB] 编排业务流程: {flow_name}")
        if flow_name == "PLACE_ORDER":
            # 步骤1：查用户（转换消息格式给 UserService）
            r1 = self.call("user", "GET_USER", {"name": params["user"]})
            if r1["status"] != "OK":
                return {"status": "FAILED", "step": "查用户"}
            # 步骤2：下单（转换消息格式给 OrderService）
            r2 = self.call("order", "CREATE", {"customer": r1["data"]["name"]})
            if r2["status"] != "OK":
                return {"status": "FAILED", "step": "下单"}
            # 步骤3：支付
            r3 = self.call("payment", "CHARGE", {"order": r2["order_id"]})
            return {"status": "OK", "result": r3}
        return {"status": "ERROR", "msg": "未知流程"}

    def show_logs(self):
        print("[ESB] 服务治理日志:")
        for log in self._logs:
            print(f"  - {log}")


# --- 服务：各用自己的术语和数据格式 ---
class UserService:
    def handle(self, action, params):
        print(f"  [UserService] 处理: {action}")
        if action == "GET_USER":
            return {"status": "OK", "data": {"name": params["name"], "tier": "gold"}}
        return {"status": "ERROR"}


class OrderService:
    def handle(self, action, params):
        print(f"  [OrderService] 处理: {action}")
        if action == "CREATE":
            return {"status": "OK", "order_id": "ORD-002", "customer": params["customer"]}
        return {"status": "ERROR"}


class PaymentService:
    def handle(self, action, params):
        print(f"  [PaymentService] 处理: {action}")
        if action == "CHARGE":
            return {"status": "OK", "txn_id": "TXN-002"}
        return {"status": "ERROR"}


# --- 运行演示 ---
if __name__ == "__main__":
    esb = ESB()
    esb.register("user", UserService())
    esb.register("order", OrderService())
    esb.register("payment", PaymentService())

    print("=" * 50)
    print("进阶演示: ESB 编排跨服务业务流程")
    print("=" * 50 + "\n")

    result = esb.orchestrate("PLACE_ORDER", {"user": "Alice"})
    print(f"\n最终结果: {result}")
    esb.show_logs()
