"""Memory（记忆架构）最小化示例

演示 Agent 三层记忆系统：
- ShortTermMemory: 短期记忆，保存近期对话，容量有限
- LongTermMemory: 长期记忆，持久知识，跨会话存活
- WorkingMemory: 工作记忆，当前任务状态"""

# --- 短期记忆：近期对话上下文 ---
class ShortTermMemory:
    """短期记忆 — 保存最近对话，容量有限，超出时丢弃最早的"""
    def __init__(self, capacity=5):
        self.capacity = capacity
        self.items = []

    def add(self, msg):
        self.items.append(msg)
        if len(self.items) > self.capacity:
            dropped = self.items.pop(0)
            print(f"[STM] 容量不足，丢弃: {dropped[:25]}...")

    def get_all(self):
        return self.items


# --- 长期记忆：跨会话持久知识 ---
class LongTermMemory:
    """长期记忆 — 持久保存重要事实"""
    def __init__(self):
        self.facts = {}

    def store(self, key, value):
        self.facts[key] = value
        print(f"[LTM] 存储: {key}={value}")

# --- 工作记忆：当前任务状态 ---
class WorkingMemory:
    """工作记忆 — 当前任务的焦点和进度"""
    def __init__(self):
        self.task = None
        self.steps = []

    def set_task(self, task):
        self.task = task; self.steps = []
        print(f"[WM] 设定任务: {task}")

# --- Agent 记忆系统：组合三层记忆 ---
class AgentMemory:
    """Agent 记忆 — 统一管理 STM、LTM、WM 三层"""
    def __init__(self):
        self.stm = ShortTermMemory(capacity=5)
        self.ltm = LongTermMemory()
        self.wm = WorkingMemory()

    def converse(self, user_msg):
        self.stm.add(f"用户: {user_msg}")
        if "喜欢" in user_msg:
            self.ltm.store("用户偏好", user_msg)


if __name__ == "__main__":
    print("=" * 50)
    print("Memory 记忆架构演示：三层记忆协作")
    print("=" * 50 + "\n")

    agent = AgentMemory()
    agent.wm.set_task("帮助用户选择编程语言")

    for msg in ["我想学编程", "我喜欢简洁的语言", "之前学过Python",
               "对并发也感兴趣", "Go适合并发吗", "还有建议吗", "谢谢"]:
        print(f"对话: {msg}")
        agent.converse(msg)

    print(f"\n[STM] 当前短期记忆({len(agent.stm.get_all())}条):")
    for item in agent.stm.get_all():
        print(f"  {item}")
    print(f"[LTM] 长期记忆: {agent.ltm.facts}")
    print(f"[WM] 任务: {agent.wm.task}")
