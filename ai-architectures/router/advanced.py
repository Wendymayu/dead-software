"""Router 进阶示例：置信度回退与嵌套路由

演示两个进阶机制：
- 置信度回退：路由分类置信度低时，回退到通用处理器
- 嵌套路由：处理器内部再次路由（code_question → python/js 专门处理）"""


# --- 一级处理器 ---
def python_handler(query):
    """Python 专门处理器"""
    print("[PythonHandler] 处理 Python 问题")
    return f"Python 解答：{query} → 建议使用 pdb 调试并检查类型"


def js_handler(query):
    """JavaScript 专门处理器"""
    print("[JSHandler] 处理 JavaScript 问题")
    return f"JS 解答：{query} → 建议检查异步逻辑和闭包作用域"


def math_handler(query):
    """数学处理器"""
    print("[MathHandler] 处理数学问题")
    return f"数学解答：{query}"


def creative_handler(query):
    """创意处理器"""
    print("[CreativeHandler] 处理创意请求")
    return f"创意回复：{query}"


def general_handler(query):
    """通用回退处理器"""
    print("[GeneralHandler] 回退处理（置信度不足）")
    return f"通用回复：关于「{query}」的参考信息"


# --- 嵌套路由：code_question 内部再分类 ---
SUB_INTENT_MAP = {"python": python_handler, "javascript": js_handler}


def classify_code_intent(query):
    """代码问题内部再路由：区分 Python vs JavaScript"""
    if "python" in query.lower() or "py" in query.lower():
        return "python"
    if "js" in query.lower() or "javascript" in query.lower():
        return "javascript"
    return "python"  # 默认归 Python


def code_router(query):
    """代码路由：先内部分类，再转发到子处理器"""
    sub_intent = classify_code_intent(query)
    sub_handler = SUB_INTENT_MAP[sub_intent]
    print(f"[CodeRouter] 内部路由: {sub_intent} → {sub_handler.__name__}")
    return sub_handler(query)


# --- 置信度分类：模拟 LLM 输出意图+置信度 ---
INTENT_MAP = {
    "code_question": code_router,
    "math_question": math_handler,
    "creative_request": creative_handler,
}


def classify_with_confidence(query):
    """分类意图并返回置信度——模糊查询置信度低"""
    if any(kw in query for kw in ["python", "js", "javascript", "代码", "bug", "函数", "编程"]):
        return "code_question", 0.92
    if any(kw in query for kw in ["计算", "求值", "数学", "等于"]):
        return "math_question", 0.95
    if any(kw in query for kw in ["写一篇", "创作", "构思"]):
        return "creative_request", 0.88
    # 模糊意图：置信度低
    return "general", 0.35


def router_agent(query, confidence_threshold=0.6):
    """RouterAgent：分类 → 置信度检查 → 路径选择 → 处理"""
    intent, confidence = classify_with_confidence(query)
    print(f"[Router] 查询: {query}")
    print(f"[Router] 意图: {intent}，置信度: {confidence:.2f}")

    if confidence < confidence_threshold:
        print(f"[Router] 置信度 < {confidence_threshold}，回退到 GeneralHandler")
        result = general_handler(query)
    else:
        handler = INTENT_MAP[intent]
        print(f"[Router] 置信度达标，路由到 {handler.__name__}")
        result = handler(query)

    print(f"[Result] {result}\n")


if __name__ == "__main__":
    print("=" * 55)
    print("Router 进阶：置信度回退与嵌套路由")
    print("=" * 55 + "\n")

    print("【场景1: 嵌套路由 — 代码问题内部再分发】")
    router_agent("这段 python 代码有 bug")
    router_agent("js 闭包导致变量泄漏")

    print("【场景2: 置信度回退 — 模糊意图兜底处理】")
    router_agent("帮我看看这个东西")

    print("--- 与基础示例对比 ---")
    print("基础示例: 每个查询都路由到唯一处理器，没有置信度判断")
    print("进阶示例: 低置信度时回退到通用处理器，代码问题内部再路由到语言专门处理器")
