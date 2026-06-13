"""Human-in-the-Loop (人机协作) 最小化示例

演示 Agent 在关键决策点暂停等待人类审批：
- Agent 提议动作并等待人类响应
- 人类可以批准、拒绝或修改提议
- 高风险操作必须有人把关才能执行"""


# --- 模拟人类审批者：自动批准或拒绝用于演示 ---
class SimulatedHuman:
    """模拟人类审批者——根据动作类型自动响应"""
    def review(self, action):
        if "删除" in action:
            return ("reject", "不允许删除数据，风险太高")
        return ("approve", "同意执行")


# --- HITL Agent：提议动作 → 等待审批 → 执行或取消 ---
class HITLAgent:
    """人机协作 Agent——关键操作需人类批准后才执行"""
    def __init__(self, human):
        self.human = human

    def propose_and_execute(self, action):
        """提议动作 → 请求人类审批 → 根据响应执行或取消"""
        print(f"[Agent] 提议动作: {action}")
        decision, reason = self.human.review(action)
        print(f"[Human] 审批结果: {decision} — {reason}")
        if decision == "approve":
            print(f"[Agent] 执行: {action}")
            return "done"
        print(f"[Agent] 取消: {action}")
        return "cancelled"


if __name__ == "__main__":
    print("=" * 50)
    print("Human-in-the-Loop 演示：Agent 等待人类审批")
    print("=" * 50 + "\n")

    agent = HITLAgent(SimulatedHuman())
    agent.propose_and_execute("查询用户列表")
    print()
    agent.propose_and_execute("删除过期数据")
