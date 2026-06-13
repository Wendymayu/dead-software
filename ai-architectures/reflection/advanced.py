"""Reflection 进阶示例：质量评分表与收敛终止

展示反思机制的两个关键特性：
- 质量评分表(Rubric)：审视不仅列出问题，还按评分维度逐项评分
- 收敛终止：当审视评分全部达标时，提前终止迭代，避免无意义的重复修改"""


# --- 评分表维度与阈值 ---
RUBRIC = {
    "准确性": {"threshold": 4, "desc": "事实是否正确"},
    "完整性": {"threshold": 3, "desc": "是否覆盖关键要点"},
    "清晰度": {"threshold": 3, "desc": "是否易于理解"},
}


# --- CriticAgent：按评分表审视回答 ---
def critic_with_rubric(response):
    """按评分表逐维度评分，返回评分和问题"""
    scores = {}
    issues = []

    # 准确性评分
    if "GIL" in response and "字节码" in response:
        scores["准确性"] = 5
    elif "GIL" in response:
        scores["准确性"] = 3
        issues.append(("准确性", "未解释 GIL 作用的层面（字节码级）"))
    else:
        scores["准确性"] = 1
        issues.append(("准确性", "缺少关键技术术语"))

    # 完整性评分
    if "例如" in response or "比如" in response:
        scores["完整性"] = 4
    elif "限制" in response:
        scores["完整性"] = 2
        issues.append(("完整性", "缺少具体例子说明影响"))
    else:
        scores["完整性"] = 1
        issues.append(("完整性", "未覆盖核心要点"))

    # 清晰度评分
    if "原因是" in response or "因为" in response:
        scores["清晰度"] = 4
    elif len(response) > 25:
        scores["清晰度"] = 2
        issues.append(("清晰度", "缺少因果解释"))
    else:
        scores["清晰度"] = 1
        issues.append(("清晰度", "回答过于简短"))

    return scores, issues


# --- RevisionAgent：针对评分不足的维度修改 ---
def revise_for_rubric(response, issues):
    """针对评分表中不达标的维度逐项修改"""
    revised = response
    for dimension, issue in issues:
        if dimension == "准确性" and "字节码" not in revised:
            revised = revised.replace("GIL", "GIL（在字节码层面）")
        if dimension == "完整性":
            revised += "。例如：计算密集型多线程受 GIL 影响无法真正并行"
        if dimension == "清晰度":
            revised += "，原因是 GIL 要求线程轮流执行而非同时执行"
    return revised


# --- 按评分表判断是否收敛 ---
def is_converged(scores):
    """所有维度评分都达到阈值 → 收敛，可终止迭代"""
    for dim, score in scores.items():
        if score < RUBRIC[dim]["threshold"]:
            return False
    return True


# --- ReflectionAgent：评分表驱动的反思循环 ---
def reflection_with_rubric(question, max_iterations=5):
    """评分表驱动反思：每次审视按维度评分，收敛时提前终止"""
    initial = "Python 多线程有并行限制"
    print(f"Question: {question}")
    print(f"Initial:  {initial}\n")

    current = initial
    for i in range(1, max_iterations + 1):
        scores, issues = critic_with_rubric(current)
        print(f"--- Iteration {i} ---")
        for dim, score in scores.items():
            threshold = RUBRIC[dim]["threshold"]
            mark = "PASS" if score >= threshold else "FAIL"
            print(f"  {dim}: {score}/{threshold} [{mark}]")
        if is_converged(scores):
            print(f"  所有维度达标 — 反思收敛，终止迭代!")
            return current
        print(f"  发现问题:")
        for dim, issue in issues:
            print(f"    [{dim}] {issue}")
        current = revise_for_rubric(current, issues)
        print(f"  Revised: {current}\n")

    print(f"达到最大迭代({max_iterations})，返回当前版本")
    return current


if __name__ == "__main__":
    print("=" * 55)
    print("Reflection 进阶：评分表驱动的反思与收敛终止")
    print("=" * 55 + "\n")

    final = reflection_with_rubric("Python 多线程为何无法真正并行？")
    print(f"\nFinal Answer: {final}")
