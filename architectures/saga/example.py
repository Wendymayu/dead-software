"""Saga 模式 (Saga Pattern) 最小化示例

演示编排式 Saga 协调三个服务的分布式事务：
- 每个步骤是本地事务，配有补偿操作
- 某步失败时，反向执行已完成步骤的补偿
"""


# --- 模拟服务：各有本地事务和补偿操作 ---
class OrderService:
    def create(self, order_id):
        print(f"  [订单] 创建订单 {order_id}")

    def cancel(self, order_id):
        print(f"  [订单] 取消订单 {order_id} ← 补偿")


class PaymentService:
    def __init__(self, fail=False):
        self.fail = fail  # 模拟支付失败

    def charge(self, order_id, amount):
        if self.fail:
            raise Exception(f"支付失败")
        print(f"  [支付] 扣款 {amount}元，订单 {order_id}")

    def refund(self, order_id, amount):
        print(f"  [支付] 退款 {amount}元，订单 {order_id} ← 补偿")


class InventoryService:
    def reserve(self, order_id, item):
        print(f"  [库存] 预留 {item}，订单 {order_id}")

    def release(self, order_id, item):
        print(f"  [库存] 释放 {item}，订单 {order_id} ← 补偿")


# --- Saga 编排器：逐步执行，失败时反向补偿 ---
class OrderSaga:
    def __init__(self, order_id, item, amount, payment_fail=False):
        self.order_id = order_id
        self.item = item
        self.amount = amount
        self.payment = PaymentService(fail=payment_fail)
        self.completed = []

    def execute(self):
        steps = [
            (OrderService().create,     OrderService().cancel,     (self.order_id,)),
            (InventoryService().reserve, InventoryService().release, (self.order_id, self.item)),
            (self.payment.charge,       self.payment.refund,       (self.order_id, self.amount)),
        ]
        for action, compensate, args in steps:
            try:
                action(*args)
                self.completed.append((compensate, args))
            except Exception as e:
                print(f"  [FAIL] {e}，启动补偿回滚")
                for c, a in reversed(self.completed):
                    c(*a)
                return False
        print(f"  [OK] Saga 完成: 订单 {self.order_id} 全部成功")
        return True


if __name__ == "__main__":
    print("=" * 40)
    print("Saga 模式演示：编排式分布式事务")
    print("=" * 40 + "\n")

    print("--- 全部成功 ---")
    OrderSaga("001", "Python书", 99).execute()
    print()

    print("--- 支付失败，反向补偿 ---")
    OrderSaga("002", "Go书", 59, payment_fail=True).execute()
