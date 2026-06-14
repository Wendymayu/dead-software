# Multi-Agent 多智能体协作

## 什么是 Multi-Agent

Multi-Agent 让多个专长不同的 Agent 协作解决问题。每个 Agent 有自己的角色和能力，通过协调者或共享通道通信，团队式分工协作。核心流程：**任务分解 → 角色分配 → 各Agent独立执行 → 结果收集 → 综合输出**。

## 核心思想

单个 Agent 能力有限，但一个团队可以覆盖研究、写作、审核、规划等多个维度。就像人类团队——不同专家贡献不同技能。

```
协调者模式：

  任务 ──→ Coordinator ──→ 分配子任务 ──→ Researcher / Writer / Reviewer ──→ 收集结果 ──→ 综合输出

去中心化模式：

  Researcher ──publish──→ Channel ──→ Writer ──publish──→ Channel ──→ Critic ──publish──→ Channel ──→ ...
                          ↑ 各Agent自主订阅感兴趣的主题，无需中心调度
```

关键特征：
- **角色专精** — 每个 Agent 只负责一个领域，简单可靠
- **分工协作** — 不同 Agent 覆盖不同维度，团队整体能力超越单Agent
- **通信机制** — 协调者模式由中心调度；去中心化模式通过共享通道通信

## 代码示例

运行基础示例：

```bash
python example.py
```

关键代码解读：

1. **ResearchAgent / WriteAgent / ReviewAgent** — 三个专精Agent，各自只处理自己擅长的子任务
2. **CoordinatorAgent** — 协调者，接收完整任务后按顺序分配子任务：研究→撰写→审核
3. **coordinator.run(task)** — 协调者依次调用各Agent，收集每步结果，最终综合输出
4. **流水线式执行** — 研究→写作→审核，前一步的输出是后一步的输入，体现Agent间的协作依赖

## 进阶示例

运行进阶示例：

```bash
python advanced.py
```

进阶示例展示两个关键机制：

1. **发布/订阅通道（Channel）** — Agent 之间通过共享 Channel 通信，无需中心协调者。各Agent自主订阅感兴趣的主题，收到消息后自动处理并发布下一步结果
2. **修订循环** — CriticAgent 发现问题时发布反馈，触发 WriteAgent 修订草稿。修订后再次提交审核，循环直到质量达标。这模拟了人类团队的"写→审→改→再审"流程

## 优缺点

**优点**
- 每个Agent聚焦单一角色——职责清晰，容易开发和调试
- 可覆盖多维度任务——研究、写作、审核、规划各有专精Agent
- 比单个Agent更可靠——多Agent交叉审核，减少单一Agent的错误
- 可并行执行——独立子任务可由不同Agent同时处理

**缺点**
- Agent间通信复杂——去中心化模式下消息传递链路难以追踪
- 协调成本高——协调者需要理解任务结构并合理分配子任务
- 可能重复工作或冲突——多个Agent可能产出矛盾的结果
- 调试困难——出问题时，是哪个Agent的错？需要逐个排查

## 业界实例

Multi-Agent 模式在主流 Agent 产品中最典型的实现是 **Devin**（Cognition Labs）。Devin 内部将编码任务拆分为多个专精 Agent：一个负责浏览网页收集信息和理解需求，一个负责编写和修改代码，一个负责运行测试并验证结果，还有一个负责审查代码质量。这些 Agent 通过共享的工作空间（浏览器状态、代码编辑器、终端输出）协作，前一个 Agent 的产出自然成为下一个 Agent 的输入。这种分工让 Devin 能处理复杂的端到端软件开发任务，从理解需求到交付可用代码。

在多 Agent 框架层面，**CrewAI** 采用角色驱动的 Crew 模式：每个 Agent 有明确的角色（如 Researcher、Writer、Reviewer）、目标和工具集。Crew 按流程编排任务——Researcher 调用搜索工具收集信息，Writer 根据研究结果撰写内容，Reviewer 审核质量并反馈修改意见。这种"研究→撰写→审核"的流水线式协作模拟了人类团队的工作方式。**AutoGPT** 则在不同子任务间分派不同的子 Agent：规划 Agent 分解目标，执行 Agent 逐项完成，评估 Agent 检验结果是否达标，未达标则触发新一轮规划，形成跨 Agent 的反思闭环。

MCP 协议本质上也是一种 Multi-Agent 思路——**Claude Code + MCP** 采用的是客户端-服务器模型，其中 MCP Server 就像专精 Agent：数据库 Server 专精数据查询，GitHub Server 专精代码仓库操作，浏览器 Server 专精网页浏览。Claude Code 作为协调者（MCP Client），根据任务需要动态连接不同的 Server，调用其专精能力完成子任务。这种模式与 CrewAI 的角色分配逻辑类似，但通过标准化协议实现——任何 MCP Server 都能被任何 MCP Client 发现和调用，无需定制集成代码。

## 真实项目中的应用 — 规角驱动的多Agent框架，每个Agent有明确角色和目标，协调者自动编排任务流程
- **AutoGen (Microsoft)** — 多Agent对话框架，Agent之间通过对话协商完成任务
- **LangGraph multi-agent** — LangGraph 的多Agent模式，用图结构编排Agent间的消息流
- **Devin** — 多Agent编码系统，不同Agent负责规划、编码、测试、调试
- **Camel** — 角色扮演式多Agent框架，两个Agent通过对话协作完成指令

## 进一步阅读

- Stanford — *"Generative Agents: Interactive Simulacra of Human Behavior"* (2023，模拟25个Agent在虚拟小镇中的社交行为)
- [AutoGen 文档](https://microsoft.github.io/autogen/) — Microsoft 多Agent对话框架的官方文档
- [CrewAI 文档](https://docs.crewai.com/) — 角角驱动的多Agent协作框架
- [LangGraph multi-agent tutorial](https://langchain-ai.github.io/langgraph/concepts/multi_agent/) — LangGraph 多Agent编排教程
