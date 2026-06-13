"""ReAct (Reason+Act) 模式最小化示例

演示 Agent 在推理(Thought)和行动(Action)之间交替循环：
- Thought: 思考下一步该做什么
- Action: 执行一个工具调用
- Observation: 观察行动结果
- 循环直到得出最终答案
"""


# --- 模拟工具：Agent 可调用的外部能力 ---
def search(query):
    """搜索工具：返回模拟搜索结果"""
    db = {"Python": "Python 是动态类型语言，1991年发布",
          "GIL": "GIL 是全局解释器锁，限制多线程并行执行",
          "ReAct": "ReAct 让 LLM 交替推理和行动，2022年由 Yao 等提出"}
    for key in db:
        if key in query:
            return db[key]
    return "未找到相关信息"


def lookup(term):
    """查找工具：在已知上下文中查找细节"""
    context = {"GIL": "GIL 使 Python 同一时刻只有一个线程执行 Python 字码",
               "Cython": "Cython 可绕过 GIL 限制实现真正的并行"}
    return context.get(term, "未找到该术语")


# --- ReAct Agent：Thought → Action → Observation 循环 ---
def react_agent(question, max_steps=5):
    """模拟 ReAct 推理循环，用预设推理路径演示核心机制"""
    # 预设推理路径：每一步是 (思考, 动作名, 动作参数)
    trace = [
        ("Python 多线程为何无法真正并行？需要找到根本原因",
         "search", "Python 多线程 GIL"),
        ("找到了 GIL 相关信息，需要深入了解 GIL 的机制",
         "lookup", "GIL"),
        ("现在理解了 GIL 机制，可以给出最终答案",
         "answer", "Python 多线程无法真正并行是因为 GIL（全局解释器锁）"
                  "限制同一时刻只有一个线程执行 Python 字码"),
    ]

    print(f"Question: {question}\n")
    for i, (thought, action, arg) in enumerate(trace[:max_steps]):
        print(f"Thought {i+1}: {thought}")
        if action == "answer":
            print(f"Action {i+1}: Answer({arg})")
            return arg
        print(f"Action {i+1}: {action}({arg})")
        obs = search(arg) if action == "search" else lookup(arg)
        print(f"Observation {i+1}: {obs}\n")
    return "未能得出答案"


if __name__ == "__main__":
    print("=" * 45)
    print("ReAct 模式演示：Thought → Action → Observation")
    print("=" * 45 + "\n")

    react_agent("Python 多线程为何无法真正并行？")
