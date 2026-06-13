"""MCP 进阶示例：多服务器连接、资源暴露与采样请求

演示三个进阶场景：
- 多服务器连接：一个客户端同时接入多个 MCP 服务器
- 资源暴露：MCP 不仅提供工具，还能暴露数据资源供 LLM 读取
- 采样请求：服务器反向请求客户端的 LLM 完成推理"""


# --- MCP 服务器：同时支持工具和资源 ---
class MCPServer:
    """MCP 服务器端，暴露工具和数据资源"""

    def __init__(self, name):
        self.name = name
        self._tools = []
        self._resources = []  # MCP 资源：供 LLM 读取的数据

    def add_tool(self, name, description, parameters, handler):
        self._tools.append({"name": name, "description": description,
                            "parameters": parameters, "handler": handler})

    def add_resource(self, uri, description, content):
        """注册资源——MCP 不仅提供动作（工具），也提供数据（资源）"""
        self._resources.append({"uri": uri, "description": description,
                                "content": content})

    def list_tools(self):
        return [{"name": t["name"], "description": t["description"],
                 "parameters": t["parameters"]} for t in self._tools]

    def list_resources(self):
        """MCP 协议方法：返回所有可读资源的描述"""
        return [{"uri": r["uri"], "description": r["description"]}
                for r in self._resources]

    def read_resource(self, uri):
        """MCP 协议方法：读取指定资源的内容"""
        for r in self._resources:
            if r["uri"] == uri:
                return r["content"]
        return f"错误：资源 '{uri}' 不存在"

    def call_tool(self, name, args):
        for t in self._tools:
            if t["name"] == name:
                return t["handler"](**args)
        return f"错误：工具 '{name}' 不存在"

    def request_sampling(self, prompt, client_llm):
        """采样：服务器反向请求客户端的 LLM 进行推理"""
        print(f"[Server '{self.name}'] 向客户端请求采样: \"{prompt}\"")
        result = client_llm(prompt)
        print(f"[Client LLM] 采样结果: \"{result}\"")
        return result


# --- 模拟 LLM 的推理能力 ---
def mock_llm(prompt):
    """模拟客户端的 LLM——服务器通过采样请求借用这个能力"""
    if "总结" in prompt:
        return "数据整体趋势向好，关键指标稳步上升"
    return f"对 '{prompt}' 的推理结果"


# --- 场景1: 多服务器连接 ---
def demo_multi_server():
    """一个 MCP 客户端同时接入两个服务器，统一发现和调用工具"""
    print("【场景1: 多服务器连接——一个客户端，多个工具源】\n")

    # 两个独立服务器，各自暴露不同工具
    weather_server = MCPServer("天气服务")
    weather_server.add_tool("get_weather", "获取城市天气", {"city": "城市名"},
                            lambda city: f"{city}: 晴天, 28°C")
    weather_server.add_tool("get_forecast", "获取3天预报", {"city": "城市名"},
                            lambda city: f"{city}: 明天多云25°C, 后天晴27°C, 大后天雨22°C")

    db_server = MCPServer("数据库服务")
    db_server.add_tool("search", "搜索数据库", {"keyword": "关键词"},
                       lambda keyword: f"找到2条关于'{keyword}'的记录")

    # 客户端同时连接两个服务器——工具跨服务器发现
    all_tools = weather_server.list_tools() + db_server.list_tools()
    print(f"[Client] 连接 2 个服务器，发现 {len(all_tools)} 个工具:")
    for t in all_tools:
        print(f"         - [{t['name']}] {t['description']}")

    print()
    # 调用时按工具名路由到对应服务器
    print("[Client] 调用 get_weather → 路由到天气服务")
    print(f"[Result] {weather_server.call_tool('get_weather', {'city': '北京'})}")
    print("[Client] 调用 search       → 路由到数据库服务")
    print(f"[Result] {db_server.call_tool('search', {'keyword': '量子计算'})}")


# --- 场景2: 资源暴露 ---
def demo_resources():
    """MCP 资源：供 LLM 读取的数据，不同于执行动作的工具"""
    print("\n【场景2: 资源暴露——MCP 不只是工具，还有数据】\n")

    server = MCPServer("知识库服务")
    server.add_resource("kb://annual-report", "2024年度报告摘要",
                        "营收增长15%, 用户数突破100万, 核心产品满意度4.8/5")
    server.add_resource("kb://team-info", "团队信息",
                        "研发团队50人, 重点方向: AI架构、数据平台、开发者工具")

    # 客户端发现可读资源
    resources = server.list_resources()
    print("[Client] 发现可读资源:")
    for r in resources:
        print(f"         - {r['uri']}: {r['description']}")

    # 读取资源内容——这是数据获取，不是工具执行
    print(f"\n[Client] 读取 kb://annual-report")
    content = server.read_resource("kb://annual-report")
    print(f"[Server] 返回: \"{content}\"")


# --- 场景3: 采样请求 ---
def demo_sampling():
    """采样：服务器反向借用客户端的 LLM 进行推理"""
    print("\n【场景3: 采样请求——服务器借用客户端的 LLM 推理】\n")

    server = MCPServer("分析服务")
    server.add_tool("analyze_data", "分析数据趋势", {"data": "数据摘要"},
                    lambda data: f"分析完成: {data}")

    # 服务器需要 LLM 推理能力，通过采样协议请求客户端
    print("[说明] 服务器处理数据时需要 LLM 总结能力，通过采样向客户端请求")
    result = server.request_sampling("总结以下数据的整体趋势: 营收增长15%, 用户破百万",
                                     mock_llm)
    print(f"[Server] 利用采样结果，完成分析: {result}")


if __name__ == "__main__":
    print("=" * 60)
    print("MCP 进阶：多服务器 / 资源暴露 / 采样请求")
    print("=" * 60 + "\n")

    demo_multi_server()
    print("\n" + "-" * 60)
    demo_resources()
    print("\n" + "-" * 60)
    demo_sampling()
