"""Prompt Chaining 进阶示例：分支链与并行链

展示两种进阶链结构：
- 分支链：根据中间结果选择不同路径（技术话题→技术链，创意话题→创意链）
- 并行链：两条链同时处理不同维度，最终合并结果
"""


# --- 共通步骤 ---
def extract_topic(raw_input):
    """步骤1：提取主题并判断类型"""
    if "算法" in raw_input or "架构" in raw_input:
        topic, type_ = "排序算法优化", "technical"
    else:
        topic, type_ = "城市记忆故事", "creative"
    print(f"  [提取主题] '{raw_input}' → 主题: '{topic}', 类型: {type_}")
    return topic, type_


# --- 技术链：适合技术类话题 ---
def tech_research(topic):
    print(f"  [技术链-研究] 查阅'{topic}'相关论文和代码实现")
    return f"{topic}的3种优化方案及性能对比数据"


def tech_outline(research):
    print(f"  [技术链-大纲] 基于研究撰写技术报告大纲")
    return "1.问题定义 2.算法分析 3.优化策略 4.实验结果 5.结论"


def tech_content(outline):
    return f"技术报告({outline})：详细分析+性能图表"


# --- 创意链：适合创意类话题 ---
def creative_research(topic):
    print(f"  [创意链-研究] 收集'{topic}'的素材和灵感")
    return f"{topic}的3个核心意象和2条叙事线索"


def creative_outline(research):
    print(f"  [创意链-大纲] 基于素材构建故事框架")
    return "1.开篇意象 2.冲突展开 3.情感高潮 4.收束回响"


def creative_content(outline):
    return f"创意作品({outline})：1200字叙事散文"


# --- 分支链：根据类型选择不同路径 ---
def branching_chain(raw_input):
    """根据主题类型走不同分支"""
    print(f"[分支链] 输入: {raw_input}\n")
    topic, type_ = extract_topic(raw_input)
    if type_ == "technical":
        print("[分支链] → 选择技术链")
        result = tech_research(topic)
        result = tech_outline(result)
        result = tech_content(result)
    else:
        print("[分支链] → 选择创意链")
        result = creative_research(topic)
        result = creative_outline(result)
        result = creative_content(result)
    print(f"\n[分支链] 输出: {result}")
    return result


# --- 并行链：两条链同时执行后合并 ---
def chain_a(task):
    """链A：处理事实核查"""
    print(f"  [链A] 分析'{task}'的事实和数据")
    return f"[链A] {task}的数据核查结果"


def chain_b(task):
    """链B：处理风格润色"""
    print(f"  [链B] 对'{task}'进行风格和表达优化")
    return f"[链B] {task}的风格润色结果"


def merge(a_result, b_result):
    """合并两条并行链的输出"""
    merged = f"合并: {a_result} + {b_result} → 最终高质量输出"
    print(f"  [合并] {merged}")
    return merged


def parallel_chain(task):
    """并行执行两条链后合并"""
    print(f"\n[并行链] 任务: {task}\n")
    a = chain_a(task)
    b = chain_b(task)
    result = merge(a, b)
    print(f"\n[并行链] 输出: {result}")
    return result


if __name__ == "__main__":
    print("=" * 50)
    print("Prompt Chaining 进阶：分支链 + 并行链")
    print("=" * 50 + "\n")

    print("--- 场景 1: 技术话题 → 技术链 ---")
    branching_chain("请写一篇关于排序算法架构优化的分析")

    print("\n--- 场景 2: 创意话题 → 创意链 ---")
    branching_chain("请创作一篇关于城市记忆的故事")

    print("\n--- 场景 3: 并行链执行 ---")
    parallel_chain("AI在医疗中的应用报告")

    print("\n--- 与基础示例对比 ---")
    print("基础示例: 5步线性链，每步依次执行")
    print("进阶示例: 分支链（条件路由）+ 并行链（多维度合并)")
