"""Saga 模式进阶示例：Temporal.io 工作流引擎

模拟 Temporal.io 的核心机制：
- WorkflowExecutor 定义有序活动步骤
- 每个活动(Activity)有重试策略和补偿(Compensation)
- 重试耗尽后，执行器按逆序运行补偿——Saga模式
"""


class Activity:
    """工作流活动：执行逻辑 + 重试策略 + 补偿逻辑"""
    def __init__(self, name, execute, compensate, max_retries=2):
        self.name, self.execute, self.compensate, self.max_retries = name, execute, compensate, max_retries


class WorkflowExecutor:
    """Temporal工作流执行器：编排活动 + 重试 + 补偿"""
    def __init__(self, name, activities):
        self.name, self.activities, self.completed = name, activities, []

    def run(self):
        print(f"[WorkflowExecutor] 启动工作流: {self.name}")
        for activity in self.activities:
            if self._retry(activity):
                self.completed.append(activity)
            else:
                print(f"  [FAIL] {activity.name} 重试耗尽, 启动补偿")
                self._compensate_all()
                return False
        print(f"[WorkflowExecutor] 工作流完成!")
        return True

    def _retry(self, activity):
        for attempt in range(1, activity.max_retries + 1):
            print(f"  [Activity] {activity.name} (尝试 {attempt}/{activity.max_retries})")
            if activity.execute():
                print(f"  [OK] {activity.name} 成功")
                return True
            print(f"  [FAIL] {activity.name} 失败, 准备重试...")
        return False

    def _compensate_all(self):
        print("  [Compensate] 按逆序执行补偿:")
        for activity in reversed(self.completed):
            print(f"  [Compensate] <- {activity.name}")
            activity.compensate()


# --- 模拟业务活动 ---
def ok_create():
    print("    -> 订单创建成功")
    return True

def ok_pay():
    print("    -> 支付扣款成功: 200元")
    return True

def fail_inventory():
    print("    -> 库存预留失败(库存不足)")
    return False

def cancel_order():
    print("    -> 订单已取消")

def refund_payment():
    print("    -> 支付已退款: 200元")

def release_inventory():
    print("    -> 库存已释放")


if __name__ == "__main__":
    print("=" * 50)
    print("Temporal.io Saga: 工作流 + 重试 + 补偿")
    print("=" * 50 + "\n")

    print("--- 失败场景(库存不足触发补偿) ---")
    WorkflowExecutor("下单流程", [
        Activity("创建订单", ok_create, cancel_order, 2),
        Activity("支付扣款", ok_pay, refund_payment, 2),
        Activity("库存预留", fail_inventory, release_inventory, 2),
    ]).run()

    print("\n--- 成功场景 ---")
    WorkflowExecutor("下单流程(成功)", [
        Activity("创建订单", lambda: (print("    -> 订单OK"), True), cancel_order, 2),
        Activity("支付扣款", lambda: (print("    -> 支付OK"), True), refund_payment, 2),
        Activity("库存预留", lambda: (print("    -> 库存OK"), True), release_inventory, 2),
    ]).run()

    print("\n核心洞察: Temporal=Saga编排器+自动重试+持久化执行, 开发者只定义活动+补偿")
