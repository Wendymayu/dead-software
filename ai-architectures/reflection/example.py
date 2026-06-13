"""Reflection（反思迭代）最小化示例

演示 Agent 生成初始输出后自我审视并迭代改进：
- ReflectionAgent: 生成回答
- CriticAgent: 审视回答，发现问题（太模糊、缺少例子等）
- RevisionAgent: 根据审视意见修改回答
- 循环直到质量达标或达到最大迭代次数"""


# --- CriticAgent：审视回答，列出问题 ---
def critic_agent(response):
    """审视回答，返回发现的问题列表"""
    issues = []
    if "模糊" in response or len(response) < 30:
        issues.append("回答太模糊，缺乏具体说明")
    if "例如" not in response and "比如" not in response:
        issues.append("缺少具体例子支撑观点")
    if "因为" not in response and "原因是" not in response:
        issues.append("没有解释原因或机制")
    return issues


# --- RevisionAgent：根据审视意见修改回答 ---
def revision_agent(response, issues):
    """根据问题列表修改回答，逐步补充内容"""
    revised = response
    for issue in issues:
        if "模糊" in issue:
            revised = "Python 的 GIL（全局解释器锁）限制了多线程并行执行"
        if "缺少具体例子" in issue:
            revised += "。例如：多线程计算密集任务时，GIL 使线程只能轮流执行"
        if "没有解释原因" in issue:
            revised += "，原因是 GIL 要求同一时刻只有一个线程执行 Python 字节码"
    return revised


# --- ReflectionAgent：生成→审视→修改循环 ---
def reflection_agent(question, max_iterations=3):
    """反思循环：生成初始回答，审视发现问题，修改后重新审视"""
    initial = "Python 多线程有点模糊的限制"
    print(f"Question: {question}")
    print(f"Initial:  {initial}\n")

    current = initial
    for i in range(1, max_iterations + 1):
        issues = critic_agent(current)
        if not issues:
            print(f"Iteration {i}: 审视通过，无问题发现 — 反思收敛!")
            return current
        print(f"Iteration {i}: 审视发现问题:")
        for issue in issues:
            print(f"  - {issue}")
        current = revision_agent(current, issues)
        print(f"Revised:  {current}\n")

    print(f"达到最大迭代次数({max_iterations})，返回当前版本")
    return current


if __name__ == "__main__":
    print("=" * 50)
    print("Reflection 反思迭代演示：生成→审视→修改→再审视")
    print("=" * 50 + "\n")

    final = reflection_agent("Python 多线程为何无法真正并行？")
    print(f"\nFinal Answer: {final}")
