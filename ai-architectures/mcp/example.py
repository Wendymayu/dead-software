"""MCP (Model Context Protocol) 最小化示例

演示 MCP 的核心机制：
- MCPServer: 用标准化 schema（name/description/parameters）暴露工具
- MCPClient: LLM 端通过协议发现并调用工具，无需知道工具实现细节
- 协议让工具和 LLM "即插即用"，就像 USB 接口"""


# --- MCP 工具 schema：协议规定的标准化描述格式 ---
class MCPServer:
    """MCP 服务器端：暴露工具，用标准化 schema 描述每个工具的能力和参数"""

    def __init__(self, name):
        self.name = name
        self._tools = []  # 每个工具都有统一的 schema

    def add_tool(self, name, description, parameters, handler):
        """注册工具——schema 是 MCP 的核心，LLM 靠它发现和理解工具"""
        self._tools.append({
            "name": name, "description": description,
            "parameters": parameters, "handler": handler,
        })

    def list_tools(self):
        """MCP 协议方法：返回所有工具的 schema（不含 handler）"""
        return [{"name": t["name"], "description": t["description"],
                 "parameters": t["parameters"]} for t in self._tools]

    def call_tool(self, name, args):
        """MCP 协议方法：根据名称调用工具，返回结果"""
        for t in self._tools:
            if t["name"] == name:
                return t["handler"](**args)
        return f"错误：工具 '{name}' 不存在"


class MCPClient:
    """MCP 客户端（LLM 端）：通过协议发现工具并调用，无需定制集成代码"""

    def __init__(self, server):
        self.server = server
        # 发现阶段：客户端通过协议获取工具列表，不需要任何硬编码
        self.available_tools = server.list_tools()
        print(f"[Client] 已连接到服务器 '{server.name}'")
        print(f"[Client] 发现 {len(self.available_tools)} 个工具:")
        for t in self.available_tools:
            print(f"         - {t['name']}: {t['description']} (参数: {t['parameters']})")

    def use_tool(self, tool_name, args):
        """调用阶段：通过协议标准接口调用，无需知道工具实现细节"""
        print(f"[Client] 调用工具 '{tool_name}'，参数: {args}")
        result = self.server.call_tool(tool_name, args)
        print(f"[Server] 返回结果: {result}")
        return result


if __name__ == "__main__":
    print("=" * 55)
    print("MCP 演示：标准化协议让工具和 LLM 即插即用")
    print("=" * 55 + "\n")

    # 服务器注册工具——只需提供标准 schema，任何 MCP 客户端都能发现
    server = MCPServer("本地服务")
    server.add_tool("get_weather", "获取城市天气", {"city": "城市名"},
                    lambda city: f"{city}: 晴天, 28°C")
    server.add_tool("calculate", "执行数学计算", {"expression": "表达式"},
                    lambda expression: str(eval(expression)))

    # 客户端连接后自动发现工具——这就是 "即插即用"
    client = MCPClient(server)

    print("\n" + "-" * 55 + "\n")
    # 调用工具——客户端通过协议调用，不关心工具在哪、怎么实现
    client.use_tool("get_weather", {"city": "北京"})
    print()
    client.use_tool("calculate", {"expression": "25*4+10"})
