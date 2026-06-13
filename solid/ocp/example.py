"""开闭原则 (OCP) 最小化示例

演示支付处理器的两种实现：
- BadPaymentProcessor 违反 OCP：每次新增支付类型都要修改
- Strategy 版本遵循 OCP：新增类型只需添加新类
"""

from abc import ABC, abstractmethod


# --- 违反 OCP ---
class BadPaymentProcessor:
    """每次新增支付方式都必须修改此类"""
    def process(self, payment_type, amount):
        if payment_type == "credit_card":
            print(f"[Bad] 信用卡支付: 元{amount}")
        elif payment_type == "alipay":
            print(f"[Bad] 支付宝支付: 元{amount}")
        # 新增微信支付？必须修改这里！违反 OCP


# --- 遵循 OCP ---
class PaymentMethod(ABC):
    @abstractmethod
    def pay(self, amount): ...


class CreditCard(PaymentMethod):
    def pay(self, amount):
        print(f"[Good] 信用卡支付: 元{amount}")


class Alipay(PaymentMethod):
    def pay(self, amount):
        print(f"[Good] 支付宝支付: 元{amount}")


class WechatPay(PaymentMethod):
    """新增支付方式——无需修改已有代码"""
    def pay(self, amount):
        print(f"[Good] 微信支付: 元{amount}")


class GoodPaymentProcessor:
    """对扩展开放，对修改关闭"""
    def __init__(self, method):
        self._method = method

    def process(self, amount):
        self._method.pay(amount)


# --- 运行演示 ---
if __name__ == "__main__":
    print("=" * 40)
    print("OCP 演示：开闭原则")
    print("=" * 40 + "\n")

    print("--- 违反 OCP ---")
    bad = BadPaymentProcessor()
    bad.process("credit_card", 100)
    bad.process("alipay", 200)
    print()

    print("--- 遵循 OCP ---")
    for method in [CreditCard(), Alipay(), WechatPay()]:
        proc = GoodPaymentProcessor(method)
        proc.process(100)
    print()

    print("关键区别：BadPaymentProcessor 新增类型需修改 if-else")
    print("GoodPaymentProcessor 新增类型只需添加新类")
