# MCP 模型上下文协议 (Model Context Protocol)

## 什么是 MCP

MCP（Model Context Protocol）是连接 LLM 与外部工具和数据源的标准化协议。任何实现 MCP 的工具都能接入任何支持 MCP 的 LLM——就像 AI 的"USB 接口"，不需要为每个工具写定制集成代码。核心流程：**MCP Server 注册工具/资源 → MCP Client 通过协议发现工具 → Client 调用工具/读取资源 → Server 执行并返回结果**。

## 核心思想

标准化接口消除碎片化。当前每个 LLM+工具组合都需要定制适配代码——GPT 用 OpenAI 的 function calling，Claude 用 Anthropic 的 tool use，每换一个 LLM 就要重新集成。MCP 定义统一协议，让工具和 LLM "即插即用"：工具只需实现 MCP Server，LLM 只需实现 MCP Client，两者通过标准 JSON-RPC 通信。

```
┌─ MCP Server A ─┐   ┌─ MCP Server B ─┐
│ 天气工具         │   │ 数据库工具       │
│ 报告资源         │   │ 搜索工具         │
└───┬───────────┘   └───┬───────────┘
    │  list_tools()      │  list_tools()
    │  call_tool()       │  list_resources()
    │  read_resource()   │  call_tool()
    │     JSON-RPC       │     JSON-RPC
    └───────┬────────────┘───────┬─────
            │                    │
        ┌───┴────────────────────┴───┐
        │      MCP Client (LLM)      │
        │  发现工具 → 选择 → 调用      │
        │  发现资源 → 读取 → 引用      │
        └────────────────────────────┘
```

关键特征：
- **标准化 schema** — 每个工具用统一格式描述（name、description、parameters），LLM 通过 schema 理解工具能力
- **协议级发现** — Client 连接 Server 后自动获取工具/资源列表，无需硬编码
- **双向通信** — 不仅能 Client 调用 Server 的工具，Server 还能通过采样请求 Client 的 LLM 推理

## 代码示例

运行基础示例：

```bash
python example.py
```

关键代码解读：

1. **MCPServer.add_tool(name, description, parameters, handler)** — 注册工具时提供标准 schema，description 和 parameters 是 LLM 发现和理解工具的依据
2. **MCPServer.list_tools()** — MCP 协议核心方法：返回工具 schema（不含实现），Client 靠它"发现"可用工具
3. **MCPClient(server)** — 连接 Server 后自动获取工具列表，这就是"即插即用"——无需为每个工具写定制代码
4. **MCPClient.use_tool()** — 通过协议标准接口调用，Client 不关心工具在哪、怎么实现

## 进阶示例

运行进阶示例：

```bash
python advanced.py
```

进阶示例展示三个实用场景：

1. **多服务器连接** — 一个 MCP Client 同时接入天气服务和数据库服务，工具跨服务器统一发现和调用，按工具名路由到对应 Server
2. **资源暴露** — MCP 不只提供动作（工具），还提供数据（资源）。Server 注册可读资源，Client 发现并读取内容——这是知识获取而非执行动作
3. **采样请求** — 服务器反向请求客户端的 LLM 进行推理。Server 处理数据时需要 LLM 总结能力，通过采样协议向 Client 请求，实现双向协作

## 优缺点

**优点**
- 标准化接口即插即用——工具一次实现，所有 MCP-compatible 的 LLM 都能用
- 工具可跨 LLM 复用——换个模型不用重写集成代码
- 减少集成开发量——统一协议替代 N×M 的定制适配矩阵
- 社区共享 MCP Server——大量开源 Server 可直接使用（数据库、API、文件系统等）

**缺点**
- 协议仍在演进中——规范和实现都可能变化，生产系统需跟进更新
- 性能开销——JSON-RPC 通信比直接函数调用慢，高频场景可能有延迟
- 安全问题——工具可访问敏感数据（数据库、文件系统），权限控制至关重要
- 不是所有 LLM 都支持——目前主要是 Claude 生态，其他模型正在跟进

## 业界实例

MCP 协议在主流 Agent 产品中最核心的实现在 **Claude Code**。Claude Code 是 MCP 协议的首个大规模生产级应用：作为 MCP Client，它可以连接多种 MCP Server 来获取专精能力——连接 PostgreSQL Server 查询数据库、连接 GitHub Server 操作代码仓库、连接浏览器 Server 访问网页信息、连接文件系统 Server 读写本地文件。Claude Code 启动时自动发现已配置 Server 的工具列表，运行中根据任务需要动态选择和调用工具，整个过程通过标准 JSON-RPC 协议完成，无需为任何工具写定制集成代码。这是 MCP "即插即用"理念的最佳验证。

在 IDE 和编辑器生态中，MCP 正在快速扩展。**Cursor** 已经开始添加 MCP 支持，让 AI 编程助手通过标准协议接入外部工具和数据源，而不是依赖自有的插件系统。**VS Code** 和 **JetBrains** 系列 IDE 也正在集成 MCP，将 MCP Server 作为 AI 工具的标准接入方式。这意味着同一个 MCP Server（比如一个数据库查询工具）可以被 Claude Code、Cursor、VS Code 等多个客户端同时使用——工具一次实现，多处复用，这正是 MCP 标准化协议的核心价值。

在 MCP Server 社区层面，已经形成了丰富的开源生态。数据库类 Server 覆盖 PostgreSQL、SQLite、MySQL 等主流数据库；API 类 Server 连接 GitHub、Slack、Jira 等开发工具；文件系统类 Server 提供安全的本地文件读写能力；还有浏览器自动化、搜索引擎、知识库检索等专用 Server。开发者可以按需组合多个 Server，为 Agent 构建定制化的工具集。**LangChain/LangGraph** 也在适配 MCP 协议，将 MCP Server 作为其 Agent 工具链的标准接入点，让 LangGraph 编排的 Agent 能通过 MCP 获取外部能力，进一步扩大了 MCP 的应用范围。

## 真实项目中的应用 — 原生支持 MCP，Claude 模型和 API 直接连接 MCP Server 使用工具和资源
- **Claude Code CLI** — 开发者工具链通过 MCP 接入外部工具（数据库查询、文件操作、API 调用等）
- **MCP Server 社区** — 大量开源 MCP Server 实现覆盖数据库（PostgreSQL、SQLite）、文件系统、GitHub API、Slack 等
- **各类 IDE 和编辑器** — VS Code、Cursor 等开始集成 MCP，让 AI 编程助手通过标准协议接入工具

## 进一步阅读

- MCP Specification — [modelcontextprotocol.io](https://modelcontextprotocol.io)（官方协议规范，定义 JSON-RPC 通信格式、工具/资源/采样三大能力）
- Anthropic MCP Docs — [docs.anthropic.com/en/docs/build-with-claude/mcp](https://docs.anthropic.com/en/docs/build-with-claude/mcp)（Claude 的 MCP 集成文档和 Server 开发指南）
- Claude Code MCP Guide — [docs.anthropic.com/en/docs/claude-code/mcp](https://docs.anthropic.com/en/docs/claude-code/mcp)（在 Claude Code CLI 中配置和使用 MCP Server 的实操指南）
