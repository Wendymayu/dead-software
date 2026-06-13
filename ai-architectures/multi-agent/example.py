"""Multi-Agent 多智能体协作最小化示例

演示多个专长不同的 Agent 协作完成任务：
- CoordinatorAgent：接收任务、分配子任务、收集结果、综合输出
- ResearchAgent：负责信息搜集
- WriteAgent：负责内容撰写
- ReviewAgent：负责质量审核
- 协调者模式：一个中心节点统一调度，各Agent专注自己的角色"""


class ResearchAgent:
    """研究Agent — 搜集与任务相关的信息"""
    def execute(self, task):
        return f"[研究结果] 关于'{task}'的核心要点：1)背景 2)现状 3)关键数据"


class WriteAgent:
    """写作Agent — 将研究结果整理成文"""
    def execute(self, task, research_result):
        return f"[草稿] 基于{research_result}，撰写关于'{task}'的分析报告"


class ReviewAgent:
    """审核Agent — 检查草稿质量"""
    def execute(self, task, draft):
        return f"[审核通过] '{task}'的报告结构清晰，内容准确"


class CoordinatorAgent:
    """协调者Agent — 分配子任务、收集结果、综合输出"""
    def __init__(self):
        self.researcher = ResearchAgent()
        self.writer = WriteAgent()
        self.reviewer = ReviewAgent()

    def run(self, task):
        # 第1步：研究Agent搜集信息
        research = self.researcher.execute(task)
        print(f"  ResearchAgent → {research}")

        # 第2步：写作Agent基于研究结果撰写草稿
        draft = self.writer.execute(task, research)
        print(f"  WriteAgent → {draft}")

        # 第3步：审核Agent检查草稿
        review = self.reviewer.execute(task, draft)
        print(f"  ReviewAgent → {review}")

        # 协调者综合输出
        return f"[最终输出] {task} → {research} → {draft} → {review}"


if __name__ == "__main__":
    print("=" * 50)
    print("Multi-Agent 演示：协调者模式下的团队协作")
    print("=" * 50 + "\n")

    coordinator = CoordinatorAgent()
    task = "AI在医疗领域的应用前景"

    print(f"任务: {task}\n")
    print("【协调者分配子任务】")
    result = coordinator.run(task)
    print(f"\n【最终综合输出】\n{result}")
