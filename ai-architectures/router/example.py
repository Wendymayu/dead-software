"""Router (路由分发) 最小化示例

演示 RouterAgent 分类用户意图并路由到专门处理器：
- Router: 分析用户查询，分类意图
- Handlers: 各意图对应的专门处理器
- 路由后处理更精确、成本更低"""


# --- 专门处理器：每个处理器专注单一领域 ---
def code_handler(query):
    """代码问题处理器"""
    print("[CodeHandler] 处理代码问题")
    return f"代码解答：{query} → 建议查阅相关 API 文档并检查语法"


def math_handler(query):
    """数学问题处理器"""
    print("[MathHandler] 处理数学问题")
    result = eval(query.replace("计算", "").strip())
    return f"数学解答：{query} → 计算结果为 {result}"


def creative_handler(query):
    """创意请求处理器"""
    print("[CreativeHandler] 处理创意请求")
    return f"创意回复：为「{query}」生成了一篇短文"


def general_handler(query):
    """通用处理器：兜底处理无法分类的请求"""
    print("[GeneralHandler] 兜底处理通用请求")
    return f"通用回复：关于「{query}」，以下是一些参考信息"


# --- Router: 分类意图 → 路由到处理器 ---
INTENT_MAP = {
    "code_question": code_handler,
    "math_question": math_handler,
    "creative_request": creative_handler,
    "general": general_handler,
}


def classify_intent(query):
    """模拟 LLM 意图分类：根据关键词判断用户意图"""
    if any(kw in query for kw in ["代码", "函数", "bug", "语法", "编程"]):
        return "code_question"
    if any(kw in query for kw in ["计算", "求值", "等于", "数学"]):
        return "math_question"
    if any(kw in query for kw in ["写一篇", "创作", "生成", "构思"]):
        return "creative_request"
    return "general"


def router_agent(query):
    """RouterAgent：分类意图 → 路由 → 处理"""
    intent = classify_intent(query)
    handler = INTENT_MAP[intent]
    print(f"[Router] 查询: {query}")
    print(f"[Router] 分类意图: {intent} → 路由到 {handler.__name__}")
    result = handler(query)
    print(f"[Result] {result}\n")


if __name__ == "__main__":
    print("=" * 50)
    print("Router 演示：意图分类 → 路由到专门处理器")
    print("=" * 50 + "\n")

    router_agent("这段 Python 代码有 bug 怎么修")
    router_agent("计算 17*23+5")
    router_agent("写一篇关于人工智能的短文")
    router_agent("今天天气怎么样")
