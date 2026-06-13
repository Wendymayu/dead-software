"""ReAct 进阶示例：处理工具失败与策略调整

当工具返回空结果时，Agent 不会直接放弃，而是：
- 观察到失败 → 思考原因 → 换一个工具或调整查询 → 再次尝试
- 这展示了 ReAct 的核心优势：推理可以指导行动策略的调整
"""


# --- 模拟工具 ---
def search(query):
    """搜索工具：部分查询会返回空结果"""
    db = {"量子计算基础": "量子计算利用量子叠加和纠缠进行并行计算",
          "量子纠缠": "量子纠缠是两个粒子状态的强关联"}
    for key in db:
        if key in query:
            return db[key]
    return None  # 搜索失败，返回 None


def lookup(term):
    """查找工具：在上下文中查找术语细节"""
    context = {"量子叠加": "量子比特可同时处于 0 和 1 的叠加状态",
               "量子纠缠": "纠缠粒子测量一个即可确定另一个的状态",
               "退相干": "量子态受环境干扰失去叠加性质，是量子计算的主要障碍"}
    return context.get(term, None)


# --- ReAct Agent with 失败处理 ---
def react_agent_with_retry(question, max_steps=6):
    """Agent 遇到工具失败时，推理调整策略并重试"""
    trace = [
        ("需要了解量子计算为何难以实用化",
         "search", "量子计算应用难点",        # 搜索失败：查询不在数据库
         None),
        ("搜索没有返回结果，查询可能太宽泛，先搜索基础概念",
         "search", "量子计算基础",             # 调整查询，重试
         "量子计算利用量子叠加和纠缠进行并行计算"),
        ("找到了基础信息，但还需要了解具体障碍，查找退相干",
         "lookup", "退相干",                   # 换用 lookup 工具
         "量子态受环境干扰失去叠加性质，是量子计算的主要障碍"),
        ("现在清楚了：退相干使量子态不稳定，这就是实用化的核心难点",
         "answer", "量子计算难以实用化，核心原因是退相干："
                   "量子态受环境干扰失去叠加性质，导致计算结果不可靠",
         None),
    ]

    print(f"Question: {question}\n")
    for i, (thought, action, arg, expected_obs) in enumerate(trace[:max_steps]):
        print(f"Thought {i+1}: {thought}")
        if action == "answer":
            print(f"Action {i+1}: Answer({arg})")
            return arg
        print(f"Action {i+1}: {action}({arg})")
        obs = search(arg) if action == "search" else lookup(arg)
        if obs is None:
            print(f"Observation {i+1}: [FAIL] 工具未返回结果\n")
        else:
            print(f"Observation {i+1}: {obs}\n")
    return "未能得出答案"


if __name__ == "__main__":
    print("=" * 50)
    print("ReAct 进阶：失败处理与策略调整")
    print("=" * 50 + "\n")

    react_agent_with_retry("量子计算为何难以实用化？")
