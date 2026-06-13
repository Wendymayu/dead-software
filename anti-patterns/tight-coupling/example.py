"""紧耦合 反模式 最小化示例

演示直接依赖具体实现 vs 依赖注入：
- OrderService 直接创建并调用 StripeGateway
- 注入版本可轻松切换支付实现
"""

from abc import ABC, abstractmethod


# --- 反模式 ---
class StripeGateway:
    def charge(self, amount):
        print(f"[Stripe] 支付 元{amount}")


class BadOrderService:
    """直接依赖具体实现——换支付就得改代码"""
    def __init__(self):
        self._gateway = StripeGateway()  # 紧耦合！

    def checkout(self, amount):
        self._gateway.charge(amount)


# --- 正确做法 ---
class PaymentGateway(ABC):
    @abstractmethod
    def charge(self, amount): ...


class StripeImpl(PaymentGateway):
    def charge(self, amount):
        print(f"[Stripe] 支付 元{amount}")


class AlipayImpl(PaymentGateway):
    def charge(self, amount):
        print(f"[Alipay] 支付 元{amount}")


class GoodOrderService:
    """依赖注入——通过构造函数传入"""
    def __init__(self, gateway: PaymentGateway):
        self._gateway = gateway  # 松耦合！

    def checkout(self, amount):
        self._gateway.charge(amount)


# --- 运行演示 ---
if __name__ == "__main__":
    print("=" * 40)
    print("紧耦合 反模式演示")
    print("=" * 40 + "\n")

    print("--- 反模式: 紧耦合 ---")
    BadOrderService().checkout(100)
    print("  换支付？改 BadOrderService.__init__")
    print()

    print("--- 正确做法: 依赖注入 ---")
    GoodOrderService(StripeImpl()).checkout(100)
    GoodOrderService(AlipayImpl()).checkout(200)
    print("  换支付？只改传入参数，OrderService 不变")

    print("\n关键：紧耦合让替换和测试困难")
    print("依赖注入实现松耦合，提高灵活性")
