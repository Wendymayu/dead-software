"""Serverless 进阶示例：函数链式调用 + 冷启动

展示两个核心特性：
1. 函数链：一个函数的输出作为事件触发下一个函数
2. 冷启动：首次调用需要初始化环境，后续调用更快
"""

import time


class ServerlessPlatform:
    """模拟 FaaS 平台，支持函数链和冷启动"""

    def __init__(self):
        self._functions = {}
        self._cold = {}  # name -> 是否处于冷状态

    def register(self, name, trigger, handler, init_time=0.0):
        self._functions[name] = {"handler": handler, "trigger": trigger, "init_time": init_time}
        self._cold[name] = True  # 新注册的函数处于冷状态

    def invoke(self, event):
        trigger_type = event["type"]
        payload = event.get("payload", {})

        for name, func in self._functions.items():
            if func["trigger"] == trigger_type:
                # 冷启动：首次调用需要初始化时间
                if self._cold[name]:
                    print(f"[Platform] 冷启动 '{name}' (初始化 {func['init_time']}s)")
                    time.sleep(func["init_time"])
                    self._cold[name] = False
                else:
                    print(f"[Platform] 热启动 '{name}' (无初始化延迟)")

                result = func["handler"](payload)
                print(f"  [{name}] 返回: {result}")

                # 如果返回结果包含 trigger，自动链式触发下一个函数
                if isinstance(result, dict) and "type" in result:
                    print(f"  [Platform] 链式触发 → 事件类型: {result['type']}")
                    self.invoke(result)

                return result

        return None


def validate_order(payload):
    """函数1：验证订单 → 输出触发下一步"""
    order_id = payload.get("order_id", "unknown")
    print(f"  [validate_order] 验证订单 {order_id} OK")
    # 返回一个新事件，触发下一个函数（函数链）
    return {"type": "queue", "payload": {"order_id": order_id, "status": "validated"}}


def pack_order(payload):
    """函数2：打包订单（被上一个函数的输出触发）"""
    order_id = payload.get("order_id", "unknown")
    print(f"  [pack_order] 打包订单 {order_id}")
    return f"订单 {order_id}: 已验证 -> 已打包 OK"


# --- 运行演示 ---
if __name__ == "__main__":
    platform = ServerlessPlatform()
    print("=" * 50)
    print("进阶演示: 函数链 + 冷启动")
    print("=" * 50 + "\n")

    # 注册函数，设置冷启动初始化时间
    platform.register("validate_order", "http", validate_order, init_time=0.05)
    platform.register("pack_order", "queue", pack_order, init_time=0.08)

    print("--- 第一次调用（冷启动）---")
    platform.invoke({"type": "http", "payload": {"order_id": "O-201"}})

    print("\n--- 第二次调用（热启动，无延迟）---")
    platform.invoke({"type": "http", "payload": {"order_id": "O-202"}})
