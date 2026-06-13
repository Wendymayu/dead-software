"""Prompt Chaining 最小化示例

演示多个提示词串联成链——每步输出作为下步输入：
- Step1: 提取主题
- Step2: 收集资料
- Step3: 撰写大纲
- Step4: 撰写内容
- Step5: 审核优化
"""


# --- 模拟各步骤：每个步骤接收上一步输出，产生新输出 ---
def extract_topic(raw_input):
    """步骤1：从原始输入中提取核心主题"""
    topic = "AI在教育领域的应用"
    print(f"  [提取主题] 输入: '{raw_input}' → 主题: '{topic}'")
    return topic


def research(topic):
    """步骤2：根据主题收集相关资料"""
    materials = f"关于'{topic}'的3篇核心论文、2个行业案例、5组关键数据"
    print(f"  [收集资料] 主题: '{topic}' → 资料: {materials}")
    return materials


def write_outline(materials):
    """步骤3：根据资料撰写大纲"""
    outline = "1.背景 2.现状分析 3.核心技术 4.案例展示 5.未来展望"
    print(f"  [撰写大纲] 资料 → 大纲: {outline}")
    return outline


def write_content(outline):
    """步骤4：根据大纲撰写正文"""
    content = f"基于大纲({outline})，完成800字分析报告"
    print(f"  [撰写内容] 大纲 → 正文: {content}")
    return content


def review(content):
    """步骤5：审核内容并提出优化建议"""
    result = f"审核'{content}' → 通过，建议补充数据图表"
    print(f"  [审核优化] 正文 → 结果: {result}")
    return result


# --- Prompt Chain：将步骤串联执行 ---
def prompt_chain(raw_input):
    """执行完整的提示词链：每步输出作为下步输入"""
    print(f"[Chain] 原始输入: {raw_input}\n")
    output = extract_topic(raw_input)
    output = research(output)
    output = write_outline(output)
    output = write_content(output)
    output = review(output)
    print(f"\n[Chain] 最终输出: {output}")
    return output


if __name__ == "__main__":
    print("=" * 50)
    print("Prompt Chaining 演示：5步内容创作链")
    print("=" * 50 + "\n")

    prompt_chain("我想了解AI在教育中的应用，写一篇分析文章")
