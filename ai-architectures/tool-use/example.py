"""Tool Use (工具调用/函数调用) 最小化示例

演示 LLM 如何选择并调用外部工具：
- 定义工具及其描述和参数规范
- Agent 分析用户意图，选择匹配的工具
- 调用工具获取结果，组合成最终响应"""


# --- 工具注册表：描述和参数规范是 LLM 选择工具的依据 ---
TOOLS = {
    "get_weather": {
        "desc": "获取指定城市的天气信息",
        "params": {"city": "城市名称"},
        "func": lambda city: f"{city}：晴天，28°C，湿度45%"
    },
    "calculate": {
        "desc": "执行数学计算",
        "params": {"expression": "数学表达式"},
        "func": lambda expression: str(eval(expression))
    },
    "search_db": {
        "desc": "从数据库中搜索信息",
        "params": {"keyword": "搜索关键词"},
        "func": lambda keyword: f"找到3条关于'{keyword}'的记录：[技术文档, 历史摘要, 相关论文]"
    },
}


# --- Agent: 意图分析 → 工具选择 → 调用 → 组合响应 ---
def analyze_intent(query):
    """模拟 LLM 从用户输入推断该调用哪个工具、传什么参数"""
    if "搜索" in query or "查询" in query:
        kw = query.replace("搜索", "").replace("查询", "").strip()
        return [("search_db", {"keyword": kw})]
    if "天气" in query or "温度" in query:
        city = query.split("城市")[-1].strip() if "城市" in query else "北京"
        return [("get_weather", {"city": city})]
    if any(op in query for op in ["计算", "+", "-", "*", "/"]):
        expr = query.replace("计算", "").strip()
        return [("calculate", {"expression": expr})]
    return [("search_db", {"keyword": query.strip()})]


def tool_use_agent(query):
    """完整 Tool Use 流程：分析意图 → 调用工具 → 组合响应"""
    print(f"[User] {query}\n")
    calls = analyze_intent(query)
    print(f"[Agent] 分析意图，决定调用: {calls}\n")

    results = {}
    for name, args in calls:
        print(f"[Agent] 调用 {name}({args})")
        result = TOOLS[name]["func"](**args)
        print(f"[Tool]  返回: {result}\n")
        results[name] = result

    # 组合工具结果为自然语言响应（模拟 LLM 的综合能力）
    response = " | ".join([f"关于「{query}」", *results.values()])
    print(f"[Agent] 最终响应: {response}")


if __name__ == "__main__":
    print("=" * 50)
    print("Tool Use 演示：LLM 选择并调用外部工具")
    print("=" * 50 + "\n")

    tool_use_agent("北京天气怎么样")
    print("\n" + "-" * 50 + "\n")
    tool_use_agent("计算 25*4+10")
    print("\n" + "-" * 50 + "\n")
    tool_use_agent("搜索 量子计算")
