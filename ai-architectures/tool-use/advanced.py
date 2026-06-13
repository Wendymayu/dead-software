"""Tool Use 进阶示例：多工具编排与错误处理

演示两个进阶场景：
- 多工具顺序调用：查询需调用多个工具，结果再组合比较
- 工具失败处理：当工具执行出错，Agent 捕获错误并调整策略"""


# --- 工具定义 ---
TOOLS = {
    "get_weather": {
        "description": "获取指定城市的天气信息",
        "parameters": {"city": "城市名称"},
        "func": lambda city: f"{city}：晴天，28°C，湿度45%"
    },
    "compare": {
        "description": "比较两组数据的差异",
        "parameters": {"data_a": "第一组数据", "data_b": "第二组数据"},
        "func": lambda data_a, data_b: f"差异：{data_a} vs {data_b}，两者温度相近，湿度差值较大"
    },
    "search_db": {
        "description": "从数据库中搜索信息",
        "parameters": {"keyword": "搜索关键词"},
        "func": lambda keyword: None if keyword == "未知主题" else f"找到2条关于'{keyword}'的记录"
    },
}


def call_tool(name, args):
    """调用工具并捕获异常——真实系统中工具可能失败"""
    tool = TOOLS[name]
    try:
        result = tool["func"](**args)
        if result is None:
            return ("error", f"工具 {name} 返回空结果，可能参数不匹配")
        return ("ok", result)
    except Exception as e:
        return ("error", f"工具 {name} 执行异常: {e}")


# --- 场景1: 多工具顺序编排 ---
def multi_tool_agent(query):
    """查询需要多个工具协作完成（如比较两个城市的天气）"""
    print(f"[User] {query}\n")
    print("[Agent] 该查询需要分步执行：先获取两个城市天气，再比较差异\n")

    # 步骤1 & 2: 并行获取两个城市的天气
    r1 = call_tool("get_weather", {"city": "北京"})
    print(f"[Agent] 调用 get_weather(北京) → [{r1[0]}] {r1[1]}")
    r2 = call_tool("get_weather", {"city": "上海"})
    print(f"[Agent] 调用 get_weather(上海) → [{r2[0]}] {r2[1]}")

    # 步骤3: 用前两步的结果调用比较工具
    r3 = call_tool("compare", {"data_a": r1[1], "data_b": r2[1]})
    print(f"[Agent] 调用 compare()     → [{r3[0]}] {r3[1]}")
    print(f"\n[Agent] 最终响应: 北京与上海天气{r3[1]}")


# --- 场景2: 工具失败时的错误处理 ---
def error_handling_agent(query):
    """工具调用失败时，Agent 不放弃，而是换用其他工具"""
    print(f"[User] {query}\n")

    # 第一次尝试：search_db 失败（关键词不在数据库中）
    r1 = call_tool("search_db", {"keyword": "未知主题"})
    print(f"[Agent] 调用 search_db(未知主题) → [{r1[0]}] {r1[1]}")

    if r1[0] == "error":
        # 策略调整：换一个更通用的关键词重新搜索
        print("[Agent] 搜索失败，调整策略：用更通用的关键词重试\n")
        r2 = call_tool("search_db", {"keyword": "量子计算"})
        print(f"[Agent] 调用 search_db(量子计算) → [{r2[0]}] {r2[1]}")
        print(f"\n[Agent] 最终响应: 经调整后，{r2[1]}")
    else:
        print(f"\n[Agent] 最终响应: {r1[1]}")


if __name__ == "__main__":
    print("=" * 55)
    print("Tool Use 进阶：多工具编排与错误处理")
    print("=" * 55 + "\n")

    print("【场景1: 多工具顺序编排】")
    multi_tool_agent("比较北京和上海的天气差异")
    print("\n" + "-" * 55 + "\n")

    print("【场景2: 工具失败处理】")
    error_handling_agent("搜索未知主题的相关信息")
