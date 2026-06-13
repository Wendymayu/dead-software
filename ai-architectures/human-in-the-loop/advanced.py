"""Human-in-the-Loop 进阶示例：三级审批模式与人类修改动作

演示三个审批模式：
- auto_approve: 低风险动作自动通过，无需等待
- require_approval: 中风险动作暂停，等待人类审批
- block: 高风险动作始终拒绝，不允许执行

还展示人类可以修改 Agent 的提议动作（而非简单批准/拒绝）"""


# --- 动作定义：名称 + 风险等级 ---
ACTIONS = [
    ("读取配置文件", "low"),
    ("发送通知邮件", "medium"),
    ("删除生产数据库", "high"),
    ("更新用户资料", "medium"),
]


# --- 三级审批策略 ---
def apply_policy(action_name, risk_level):
    """根据风险等级决定审批策略"""
    if risk_level == "low":
        return ("auto_approve", "低风险，自动通过")
    if risk_level == "medium":
        return ("require_approval", "中风险，需人类审批")
    return ("block", "高风险，禁止执行")


# --- 模拟人类审批者：可批准、拒绝或修改动作 ---
class SimulatedHuman:
    """模拟人类审批——可批准、拒绝或修改提议"""
    def review(self, action_name, risk_level):
        if action_name == "发送通知邮件":
            # 人类修改提议：把"发送通知邮件"改为"发送内部测试邮件"
            return ("modify", "发送内部测试邮件", "先在内部测试，再正式发送")
        if action_name == "更新用户资料":
            return ("approve", "确认更新安全")
        return ("reject", "拒绝该操作")


# --- HITL Agent with 三级审批 ---
class HITLAgent:
    """人机协作 Agent——三级审批 + 人类可修改提议"""
    def __init__(self, human):
        self.human = human

    def execute(self, action_name, risk_level):
        """策略判定 → 人类审批 → 执行/取消/修改后执行"""
        policy, reason = apply_policy(action_name, risk_level)
        print(f"[Agent] 动作: {action_name} | 风险: {risk_level} → 策略: {policy}")

        if policy == "auto_approve":
            print(f"[Agent] 自动通过 — {reason}")
            print(f"[Agent] 执行: {action_name}")
            return

        if policy == "block":
            print(f"[Agent] 禁止执行 — {reason}")
            return

        # require_approval: 请求人类审批
        human_resp = self.human.review(action_name, risk_level)
        if human_resp[0] == "approve":
            print(f"[Human] 批准 — {human_resp[1]}")
            print(f"[Agent] 执行: {action_name}")
        elif human_resp[0] == "modify":
            modified_action, mod_reason = human_resp[1], human_resp[2]
            print(f"[Human] 修改提议 — {mod_reason}")
            print(f"[Human] 原提议: {action_name} → 修改为: {modified_action}")
            print(f"[Agent] 执行修改后的动作: {modified_action}")
        else:
            print(f"[Human] 拒绝 — {human_resp[1]}")


if __name__ == "__main__":
    print("=" * 55)
    print("HITL 进阶：三级审批模式 + 人类可修改提议")
    print("=" * 55 + "\n")

    agent = HITLAgent(SimulatedHuman())
    for name, risk in ACTIONS:
        agent.execute(name, risk)
        print()
