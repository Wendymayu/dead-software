"""Planning (目标分解) 最小化示例

演示 PlanningAgent 接收高层目标，分解为子任务序列，逐步执行：
- 将"规划东京旅行"分解为研究航班、查找酒店、查看天气、计算预算
- 使用任务注册表(Registry)映射子任务到具体执行函数
"""


# --- 子任务注册表：每个子任务对应一个执行函数 ---
def research_flights(goal):
    print(f"  [航班] 搜索东京航班，找到 3200元 的机票")


def find_hotels(goal):
    print(f"  [酒店] 查找东京酒店，找到 500元/晚 的住宿")


def check_weather(goal):
    print(f"  [天气] 查看东京天气，预计晴朗 25度")


def calculate_budget(goal):
    print(f"  [预算] 计算总费用: 航班 3200元 + 酒店 1500元 + 其他 800元 = 5500元")


TASK_REGISTRY = {
    "研究航班": research_flights,
    "查找酒店": find_hotels,
    "查看天气": check_weather,
    "计算预算": calculate_budget,
}


# --- PlanningAgent：接收目标 → 分解子任务 → 逐步执行 ---
class PlanningAgent:
    def __init__(self, registry):
        self.registry = registry

    def plan(self, goal):
        """将高层目标分解为子任务序列"""
        print(f"[Planning] 收到目标: {goal}")
        subtasks = ["研究航班", "查找酒店", "查看天气", "计算预算"]
        print(f"[Planning] 分解为 {len(subtasks)} 个子任务: {subtasks}")
        return subtasks

    def execute(self, goal, subtasks):
        """逐步执行计划中的每个子任务"""
        for i, task in enumerate(subtasks, 1):
            print(f"\n[Planning] 步骤 {i}/{len(subtasks)}: {task}")
            self.registry[task](goal)
        print(f"\n[Planning] [OK] 计划全部完成")


if __name__ == "__main__":
    print("=" * 40)
    print("Planning 演示：目标分解与逐步执行")
    print("=" * 40 + "\n")

    agent = PlanningAgent(TASK_REGISTRY)
    subtasks = agent.plan("规划东京旅行")
    agent.execute("规划东京旅行", subtasks)
