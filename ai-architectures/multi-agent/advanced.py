"""Multi-Agent 进阶示例：去中心化通信与审核修订循环

展示两个进阶机制：
- 发布/订阅通道：Agent 之间通过共享 Channel 通信，无需中心协调者
- 修订循环：CriticAgent 发现问题后发布反馈，触发 WriteAgent 修订，循环直到质量达标"""


class Channel:
    """共享通信通道 — Agent 发布消息，订阅者自动接收"""
    def __init__(self):
        self.subscribers = {}  # topic → [agent]

    def subscribe(self, topic, agent):
        if topic not in self.subscribers:
            self.subscribers[topic] = []
        self.subscribers[topic].append(agent)

    def publish(self, topic, message):
        for agent in self.subscribers.get(topic, []):
            agent.receive(topic, message)


class Agent:
    """基础Agent — 有名字，能订阅和接收消息"""
    def __init__(self, name):
        self.name = name
        self.received = []

    def receive(self, topic, message):
        self.received.append((topic, message))
        print(f"  [{self.name}] 收到 {topic}: {message}")


class ResearchAgent(Agent):
    def __init__(self, channel):
        super().__init__("Researcher")
        self.channel = channel
        channel.subscribe("task", self)

    def receive(self, topic, message):
        super().receive(topic, message)
        # 收到任务后，发布研究结果
        result = f"[研究完成] 关于'{message}'的核心发现"
        self.channel.publish("research", result)


class WriteAgent(Agent):
    """写作Agent — 可根据审核反馈修订草稿"""
    def __init__(self, channel, max_revisions=2):
        super().__init__("Writer")
        self.channel = channel
        self.max_revisions = max_revisions
        self.revision_count = 0
        channel.subscribe("research", self)
        channel.subscribe("feedback", self)

    def receive(self, topic, message):
        super().receive(topic, message)
        if topic == "research":
            draft = f"[初稿] 基于{message}的分析报告"
            self.revision_count = 0
            self.channel.publish("draft", draft)
        elif topic == "feedback":
            self.revision_count += 1
            if self.revision_count <= self.max_revisions:
                revised = f"[修订稿v{self.revision_count}] 已根据反馈调整"
                self.channel.publish("draft", revised)


class CriticAgent(Agent):
    """审核Agent — 发现问题就发布反馈，触发修订循环"""
    def __init__(self, channel, issues=1):
        super().__init__("Critic")
        self.channel = channel
        self.issues = issues
        self.reviewed = 0
        channel.subscribe("draft", self)

    def receive(self, topic, message):
        super().receive(topic, message)
        self.reviewed += 1
        if self.reviewed <= self.issues:
            # 发现问题，发布反馈触发修订
            self.channel.publish("feedback", f"[反馈] 第{self.reviewed}次审核：需补充数据支撑")
        else:
            # 审核通过，发布最终确认
            self.channel.publish("final", f"[审核通过] 报告质量达标")


if __name__ == "__main__":
    print("=" * 50)
    print("Multi-Agent 进阶：去中心化通信 + 修订循环")
    print("=" * 50 + "\n")

    channel = Channel()
    researcher = ResearchAgent(channel)
    writer = WriteAgent(channel, max_revisions=2)
    critic = CriticAgent(channel, issues=1)

    # 模拟一个最终订阅者接收结果
    final = Agent("Final")
    channel.subscribe("final", final)

    print("【发布初始任务】\n")
    channel.publish("task", "AI在医疗领域的应用前景")

    print(f"\n【最终结果】{final.received[-1][1]}")

    print("\n--- 与基础示例对比 ---")
    print("基础示例: 协调者统一调度，Agent之间不直接通信")
    print("进阶示例: Agent通过Channel自主通信，Critic可触发修订循环")
