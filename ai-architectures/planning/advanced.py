"""Planning 进阶示例：计划修订与动态调整

演示当子任务失败时，Agent 修订计划而非放弃整个目标：
- 航班太贵 → 替换为"查找替代日期航班"
- 中间结果影响后续步骤 → 天气恶劣 → 调整酒店为室内活动型
"""


# --- 子任务执行函数，部分可配置为失败 ---
def research_flights(fail=False):
    if fail:
        print("  [航班] 搜索东京航班... 8000元 太贵！超出预算")
        raise Exception("航班价格超出预算上限 5000元")
    print("  [航班] 搜索东京航班，找到 3200元 的机票")
    return {"flight_price": 3200}


def find_alt_flights():
    print("  [航班] 尝试替代日期... 找到 2800元 的机票（错峰出行）")
    return {"flight_price": 2800}


def find_hotels(prefer_indoor=False):
    if prefer_indoor:
        print("  [酒店] 天气不佳，选择室内活动型酒店（带温泉和商场）")
    else:
        print("  [酒店] 查找东京酒店，找到 500元/晚 的住宿")
    return {"hotel_price": 500}


def check_weather(bad=False):
    if bad:
        print("  [天气] 东京预计连续暴雨!")
        return {"bad_weather": True}
    print("  [天气] 东京预计晴朗 25度")
    return {"bad_weather": False}


def calculate_budget(results):
    flight = results.get("flight_price", 0)
    hotel = results.get("hotel_price", 0)
    total = flight + hotel * 3 + 800
    print(f"  [预算] 总费用: 航班 {flight}元 + 酒店 {hotel}元×3 + 其他 800元 = {total}元")


# --- PlanningAgent：支持计划修订 ---
class PlanningAgent:
    def __init__(self):
        self.plan = []
        self.results = {}

    def make_plan(self, goal):
        print(f"[Planning] 收到目标: {goal}")
        self.plan = ["研究航班", "查看天气", "查找酒店", "计算预算"]
        print(f"[Planning] 初始计划: {self.plan}")
        return self.plan

    def execute(self, flight_fail=False, bad_weather=False):
        for i, task in enumerate(self.plan):
            print(f"\n[Planning] 步骤 {i+1}/{len(self.plan)}: {task}")
            try:
                if task == "研究航班":
                    r = research_flights(fail=flight_fail)
                    self.results.update(r)
                elif task == "查找替代航班":
                    r = find_alt_flights()
                    self.results.update(r)
                elif task == "查找酒店":
                    indoor = self.results.get("bad_weather", False)
                    r = find_hotels(prefer_indoor=indoor)
                    self.results.update(r)
                elif task == "查看天气":
                    r = check_weather(bad=bad_weather)
                    self.results.update(r)
                    # 动态调整：天气差 → 重新安排酒店
                    if r.get("bad_weather"):
                        print("[Planning] 天气不佳，修订计划：调整酒店选择")
                elif task == "计算预算":
                    calculate_budget(self.results)
            except Exception as e:
                print(f"[Planning] [FAIL] {e} → 修订计划")
                # 修订：在失败位置插入替代方案
                self.plan[i] = "查找替代航班"
                print(f"[Planning] 新计划: {self.plan}")
                return self.execute_from(i)  # 从失败步骤重新执行
        print(f"\n[Planning] [OK] 计划全部完成")

    def execute_from(self, start):
        """从指定步骤重新执行修订后的计划"""
        for i in range(start, len(self.plan)):
            task = self.plan[i]
            print(f"\n[Planning] 步骤 {i+1}/{len(self.plan)}: {task}")
            if task == "查找替代航班":
                self.results.update(find_alt_flights())
            elif task == "查找酒店":
                indoor = self.results.get("bad_weather", False)
                self.results.update(find_hotels(prefer_indoor=indoor))
            elif task == "计算预算":
                calculate_budget(self.results)
        print(f"\n[Planning] [OK] 修订后计划全部完成")


if __name__ == "__main__":
    print("=" * 50)
    print("Planning 进阶：计划修订与动态调整")
    print("=" * 50 + "\n")

    print("--- 场景 1: 航班太贵 → 修订计划查找替代 ---")
    agent = PlanningAgent()
    agent.make_plan("规划东京旅行")
    agent.execute(flight_fail=True)
    print()

    print("--- 场景 2: 天气恶劣 → 动态调整酒店选择 ---")
    agent2 = PlanningAgent()
    agent2.make_plan("规划东京旅行")
    agent2.execute(bad_weather=True)
