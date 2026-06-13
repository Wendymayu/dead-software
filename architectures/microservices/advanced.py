"""微服务进阶示例：服务发现与熔断

展示微服务架构中的关键问题：
- 服务发现：服务自动注册，客户端动态发现
- 简单熔断：当服务不可用时，快速失败而非无限等待
"""

import time


class ServiceRegistry:
    """服务发现注册中心"""

    def __init__(self):
        self._services = {}

    def register(self, name, service, healthy=True):
        self._services[name] = {"service": service, "healthy": healthy}
        print(f"  [Registry] '{name}' 已注册 (healthy={healthy})")

    def discover(self, name):
        entry = self._services.get(name)
        if entry and entry["healthy"]:
            return entry["service"]
        print(f"  [Registry] '{name}' 不可用!")
        return None

    def set_health(self, name, healthy):
        if name in self._services:
            self._services[name]["healthy"] = healthy
            status = "恢复" if healthy else "故障"
            print(f"  [Registry] '{name}' 状态: {status}")


class CircuitBreaker:
    """简单熔断器：连续失败2次后断开，2秒后尝试恢复"""

    def __init__(self, failure_threshold=2, recovery_timeout=2):
        self._failures = 0
        self._threshold = failure_threshold
        self._open = False
        self._last_failure_time = 0
        self._recovery_timeout = recovery_timeout

    def call(self, func):
        if self._open:
            if time.time() - self._last_failure_time > self._recovery_timeout:
                print("  [熔断器] 半开状态，尝试恢复...")
                self._open = False
            else:
                print("  [熔断器] 断开! 快速失败")
                return {"error": "circuit_breaker_open"}
        try:
            result = func()
            self._failures = 0
            return result
        except Exception as e:
            self._failures += 1
            print(f"  [熔断器] 失败计数: {self._failures}")
            if self._failures >= self._threshold:
                self._open = True
                self._last_failure_time = time.time()
                print("  [熔断器] 达到阈值，断开!")
            return {"error": str(e)}


# --- 模拟服务 ---
class GoodService:
    def handle(self, method, params):
        return {"status": "ok", "data": "正常响应"}


class BrokenService:
    def handle(self, method, params):
        raise RuntimeError("服务内部错误")


# --- 运行演示 ---
if __name__ == "__main__":
    registry = ServiceRegistry()
    breaker = CircuitBreaker(failure_threshold=2, recovery_timeout=2)

    print("=" * 50)
    print("进阶演示：服务发现 + 熔断保护")
    print("=" * 50 + "\n")

    # 注册服务
    print("--- 服务注册 ---")
    registry.register("good-service", GoodService())
    registry.register("bad-service", BrokenService())
    print()

    # 正常调用
    print("--- 正常调用 ---")
    svc = registry.discover("good-service")
    result = breaker.call(lambda: svc.handle("ping", {}))
    print(f"  结果: {result}\n")

    # 故障服务（触发熔断）
    print("--- 故障服务（触发熔断）---")
    svc = registry.discover("bad-service")
    breaker.call(lambda: svc.handle("ping", {}))
    breaker.call(lambda: svc.handle("ping", {}))
    breaker.call(lambda: svc.handle("ping", {}))  # 应被熔断器拦截
