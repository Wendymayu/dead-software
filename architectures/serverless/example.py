"""Serverless (无服务器架构) 最小化示例

模拟 FaaS 平台：开发者注册函数，平台根据事件触发类型路由到对应函数。
函数不关心运行环境，平台负责部署、扩展、容错。
"""


class FunctionRegistry:
    """无服务器平台：注册函数并根据事件触发类型路由"""

    def __init__(self):
        self._functions = {}  # name -> {"handler": fn, "trigger": type}

    def register(self, name, trigger, handler):
        """注册函数：name=函数名, trigger=触发类型(http/queue/timer), handler=业务逻辑"""
        self._functions[name] = {"handler": handler, "trigger": trigger}
        print(f"  [Platform] 注册函数: {name} (触发类型: {trigger})")

    def invoke(self, event):
        """接收事件，路由到匹配触发类型的函数"""
        trigger_type = event["type"]
        payload = event.get("payload", {})

        for name, func in self._functions.items():
            if func["trigger"] == trigger_type:
                print(f"[Platform] 事件 '{trigger_type}' → 触发函数 '{name}'")
                result = func["handler"](payload)
                print(f"  [Platform] 函数 '{name}' 返回: {result}")
                return result

        print(f"[Platform] 无匹配函数处理事件类型: {trigger_type}")
        return None


def hello(payload):
    """业务函数：HTTP 触发，返回问候"""
    name = payload.get("name", "World")
    return f"Hello, {name}!"


def process_order(payload):
    """业务函数：队列触发，处理订单"""
    order_id = payload.get("order_id", "unknown")
    item = payload.get("item", "unknown item")
    return f"订单 {order_id} 已处理: {item}"


# --- 运行演示 ---
if __name__ == "__main__":
    platform = FunctionRegistry()
    print("=" * 40)
    print("Serverless 演示: 注册函数 → 事件触发 → 自动路由")
    print("=" * 40 + "\n")

    # 开发者只写函数，平台负责注册和路由
    platform.register("hello", "http", hello)
    platform.register("process_order", "queue", process_order)

    print()

    # 模拟事件到达平台
    platform.invoke({"type": "http", "payload": {"name": "Alice"}})
    platform.invoke({"type": "queue", "payload": {"order_id": "O-101", "item": "键盘"}})
