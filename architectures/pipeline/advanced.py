"""管道架构进阶示例：分支管道与错误处理

展示更复杂的管道场景：
- 分支管道：根据条件选择不同处理路径
- 错误处理：某个阶段失败后的处理策略
"""


def validate(data):
    errors = []
    if not data.get("text"):
        errors.append("缺少文本")
    if len(data.get("text", "")) < 3:
        errors.append("文本过短")
    data["errors"] = errors
    data["valid"] = len(errors) == 0
    return data


def route(data):
    """根据语言分支到不同处理管道"""
    text = data.get("text", "")
    if any(ord(c) > 0x4E00 for c in text):
        data["route"] = "chinese"
    else:
        data["route"] = "english"
    return data


def process_chinese(data):
    data["processed"] = f"[中文处理] {data['text']}"
    return data


def process_english(data):
    data["processed"] = f"[英文处理] {data['text'].upper()}"
    return data


def error_handler(data):
    """错误处理阶段"""
    if data.get("errors"):
        print(f"  [错误处理] 发现错误: {data['errors']}")
        data["processed"] = f"[错误] {', '.join(data['errors'])}"
    return data


def run_pipeline(data, stages):
    for stage in stages:
        print(f"  → {stage.__name__}")
        data = stage(data)
    return data


# --- 运行演示 ---
if __name__ == "__main__":
    print("=" * 50)
    print("进阶演示：分支管道 + 错误处理")
    print("=" * 50 + "\n")

    # 英文文本
    print("--- 英文路径 ---")
    result = run_pipeline({"text": "hello world"},
                          [validate, route, process_english])
    print(f"  结果: {result}\n")

    # 中文文本
    print("--- 中文路径 ---")
    result = run_pipeline({"text": "你好世界"},
                          [validate, route, process_chinese])
    print(f"  结果: {result}\n")

    # 错误数据
    print("--- 错误路径 ---")
    result = run_pipeline({"text": "ab"},
                          [validate, error_handler])
    print(f"  结果: {result}")
