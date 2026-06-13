"""管道/过滤器架构 (Pipeline Architecture) 最小化示例

演示数据经过多个处理阶段（过滤器）逐步流转：
- 每个过滤器接收输入，处理后传给下一个
- 过滤器之间独立，只通过数据传递连接
"""


# --- 过滤器：每个阶段处理数据并传递 ---
def validate(data):
    """验证数据完整性"""
    print(f"  [验证] 检查数据: {data}")
    if not data.get("text"):
        data["errors"] = data.get("errors", []) + ["缺少文本内容"]
    data["validated"] = True
    return data


def normalize(data):
    """标准化文本"""
    print(f"  [标准化] 处理文本")
    data["text"] = data["text"].lower().strip()
    data["normalized"] = True
    return data


def enrich(data):
    """丰富数据：添加元信息"""
    print(f"  [丰富] 添加元信息")
    data["word_count"] = len(data["text"].split())
    data["enriched"] = True
    return data


# --- 管道：串联过滤器 ---
def pipeline(data, filters):
    """将数据依次通过所有过滤器"""
    print(f"[Pipeline] 开始处理，共 {len(filters)} 个阶段\n")
    for i, filter_fn in enumerate(filters, 1):
        print(f"  --- 阶段 {i}: {filter_fn.__name__} ---")
        data = filter_fn(data)
    print(f"\n[Pipeline] 处理完成")
    return data


# --- 运行演示 ---
if __name__ == "__main__":
    print("=" * 40)
    print("管道架构演示：数据逐步通过多个过滤器")
    print("=" * 40 + "\n")

    input_data = {"text": "  Hello World of Software Engineering  "}
    filters = [validate, normalize, enrich]

    result = pipeline(input_data, filters)
    print(f"\n最终输出: {result}")
