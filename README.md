# Dead-Software

> 软件工程架构与设计模式的阅读资料，配有简单但可运行的代码示例。

## 为什么有这个项目

AI coding 正在深刻改变软件工程——代码生成、调试、重构，AI 都能做，而且做得越来越快。

但这带来一个隐患：**新入门的工程师可能跳过了传统的成长经历**。过去，你在反复手写和踩坑中自然建立起对架构和设计的判断力——什么时候该用微服务，什么时候分层就够了；哪段代码藏着紧耦合，哪种抽象其实是过度设计。这些判断力不是来自"会写代码"，而是来自"写过很多代码后知道什么代码不该写"。

AI 让你不再需要"手熟"，但反而更需要"眼毒"。

- 手写代码的能力贬值了——AI 比你快、比你不犯错
- 判断代码的能力升值了——AI 给你方案，但你得判断这个方案在你的场景下是否合理
- 架构选择的权力还在你手里——AI 不知道你的团队大小、业务阶段、组织约束

**判断力的来源，就是对架构和设计模式的轮廓理解**——不是每个实现细节，而是每个模式的：为什么存在、什么场景适用、有什么代价。

这正是这个项目要做的事：**不是教你写代码，而是帮你建立判断力。**

项目名 "dead-software" 不是一个悲观的名字。它是一个提醒——传统的"手写软件"方式正在消亡，但软件工程的思想不会。理解这些思想，你才能在 AI coding 时代做一个有判断力的工程师，而不是一个只会点确认按钮的操作员。

## 项目简介

本项目完整覆盖软件工程的核心知识体系，全部 62 个主题已完成，配有简洁讲解和最小化可运行代码：

- **架构模式**（22） — 分层、事件驱动、微服务、管道、单体、MVC、MVP、MVVM、六边形、客户端-服务器、SOA、CQRS、无服务器、插件、微内核、对等网络、Actor、事件溯源、绞杀者、Saga、黑板、REST
- **设计模式**（15） — 观察者、策略、工厂、装饰器、单例、适配器、命令、代理、外观、组合、桥接、模板方法、状态、迭代器、责任链
- **AI & Agent 架构**（12） — RAG、ReAct、Tool Use、Prompt Chaining、Router、Planning、Reflection、Multi-Agent、Memory、Guardrails、Human-in-the-Loop、MCP
- **SOLID 原则**（5） — SRP、OCP、LSP、ISP、DIP
- **并发模式**（4） — 生产者-消费者、Reactor、读写锁、Future/Promise
- **反模式**（4） — God Object、紧耦合、过早优化、复制粘贴编程

每个主题不需要你手写实现，而是让你读完之后能回答三个问题：**它解决什么问题？什么时候该用？用了要付出什么代价？**

完整主题规划见 [docs/roadmap.md](docs/roadmap.md)。

## 如何使用

每个主题目录包含：
- `README.md` — 概念讲解、优缺点、真实项目应用、延伸阅读
- `example.py` — 最小化可运行示例（`python example.py` 即可运行）
- `advanced.py` — 进阶示例（部分主题提供）

不需要安装任何依赖：

```bash
python architectures/layered/example.py
python design-patterns/observer/example.py
```

## 已完成主题

### 架构模式 (22)

| 主题 | 目录 | 核心演示 |
|------|------|----------|
| 分层架构 | [architectures/layered/](architectures/layered/) | 三层分离（展示层/业务层/数据层） |
| 事件驱动架构 | [architectures/event-driven/](architectures/event-driven/) | 事件总线 + 发布订阅 |
| 微服务架构 | [architectures/microservices/](architectures/microservices/) | 独立服务通过 HTTP 通信 |
| 管道架构 | [architectures/pipeline/](architectures/pipeline/) | 数据经过多个处理阶段流转 |
| 单体架构 | [architectures/monolithic/](architectures/monolithic/) | 所有功能在一个应用中 |
| MVC | [architectures/mvc/](architectures/mvc/) | Model-View-Controller 三角分离 |
| MVP | [architectures/mvp/](architectures/mvp/) | View 与 Model 完全隔离 |
| MVVM | [architectures/mvvm/](architectures/mvvm/) | 数据绑定驱动视图 |
| 六边形架构 | [architectures/hexagonal/](architectures/hexagonal/) | 端口与适配器，核心不依赖外部 |
| 客户端-服务器 | [architectures/client-server/](architectures/client-server/) | 客户端发起请求，服务器响应 |
| SOA | [architectures/soa/](architectures/soa/) | 服务通过标准契约协作 |
| CQRS | [architectures/cqrs/](architectures/cqrs/) | 命令与查询分离，读写模型独立 |
| 无服务器架构 | [architectures/serverless/](architectures/serverless/) | 函数即服务，按调用计费 |
| 插件架构 | [architectures/plugin/](architectures/plugin/) | 核心系统动态加载扩展 |
| 微内核 | [architectures/microkernel/](architectures/microkernel/) | 最小核心 + 可选功能扩展 |
| 对等网络 | [architectures/peer-to-peer/](architectures/peer-to-peer/) | 节点既是客户端又是服务器 |
| Actor 模型 | [architectures/actor/](architectures/actor/) | 独立状态+邮箱，消息通信 |
| 事件溯源 | [architectures/event-sourcing/](architectures/event-sourcing/) | 以事件序列替代传统状态存储 |
| 绞杀者模式 | [architectures/strangler/](architectures/strangler/) | 逐步用新系统替换旧系统 |
| Saga | [architectures/saga/](architectures/saga/) | 微服务下的分布式长事务协调 |
| 黑板架构 | [architectures/blackboard/](architectures/blackboard/) | 多专家通过共享黑板协同求解 |
| REST 架构 | [architectures/rest/](architectures/rest/) | 资源 + 统一接口 + 无状态通信 |

### 设计模式 (15)

| 主题 | 目录 | 核心演示 |
|------|------|----------|
| 观察者模式 | [design-patterns/observer/](design-patterns/observer/) | 一对多依赖通知 |
| 策略模式 | [design-patterns/strategy/](design-patterns/strategy/) | 算法族可互换封装 |
| 工厂模式 | [design-patterns/factory/](design-patterns/factory/) | 对象创建逻辑集中管理 |
| 装饰器模式 | [design-patterns/decorator/](design-patterns/decorator/) | 动态给对象添加职责 |
| 单例模式 | [design-patterns/singleton/](design-patterns/singleton/) | 全局唯一实例 |
| 适配器模式 | [design-patterns/adapter/](design-patterns/adapter/) | 不兼容接口之间的转换桥接 |
| 命令模式 | [design-patterns/command/](design-patterns/command/) | 将操作封装为对象 |
| 代理模式 | [design-patterns/proxy/](design-patterns/proxy/) | 为对象提供替代品以控制访问 |
| 外观模式 | [design-patterns/facade/](design-patterns/facade/) | 为复杂子系统提供简化接口 |
| 组合模式 | [design-patterns/composite/](design-patterns/composite/) | 树形结构的统一处理 |
| 桥接模式 | [design-patterns/bridge/](design-patterns/bridge/) | 将抽象与实现分离 |
| 模板方法 | [design-patterns/template-method/](design-patterns/template-method/) | 父类定义骨架，子类填充步骤 |
| 状态模式 | [design-patterns/state/](design-patterns/state/) | 对象行为随内部状态变化 |
| 迭代器模式 | [design-patterns/iterator/](design-patterns/iterator/) | 顺序访问集合元素 |
| 责任链模式 | [design-patterns/chain-of-responsibility/](design-patterns/chain-of-responsibility/) | 请求沿处理链传递 |

### AI & Agent 架构 (12)

| 主题 | 目录 | 核心演示 |
|------|------|----------|
| RAG | [ai-architectures/rag/](ai-architectures/rag/) | 查询 → 检索外部知识 → 增强生成 |
| ReAct | [ai-architectures/react/](ai-architectures/react/) | 思考→行动→观察循环 |
| Tool Use | [ai-architectures/tool-use/](ai-architectures/tool-use/) | LLM 选择并调用外部工具 |
| Prompt Chaining | [ai-architectures/prompt-chaining/](ai-architectures/prompt-chaining/) | 多提示词串联 |
| Router | [ai-architectures/router/](ai-architectures/router/) | 分类意图 → 路由到专门处理器 |
| Planning | [ai-architectures/planning/](ai-architectures/planning/) | 分解目标为子任务、逐步执行 |
| Reflection | [ai-architectures/reflection/](ai-architectures/reflection/) | 自我审视并迭代改进 |
| Multi-Agent | [ai-architectures/multi-agent/](ai-architectures/multi-agent/) | 多个专长 Agent 协作 |
| Memory | [ai-architectures/memory/](ai-architectures/memory/) | 短期对话记忆 + 长期知识存储 |
| Guardrails | [ai-architectures/guardrails/](ai-architectures/guardrails/) | 输入/输出验证层，约束行为边界 |
| Human-in-the-Loop | [ai-architectures/human-in-the-loop/](ai-architectures/human-in-the-loop/) | 关键决策点等待人类审批 |
| MCP | [ai-architectures/mcp/](ai-architectures/mcp/) | 标准化协议连接 LLM 与外部工具 |

### SOLID 原则 (5)

| 主题 | 目录 | 核心演示 |
|------|------|----------|
| 单一职责原则 | [solid/srp/](solid/srp/) | 一个类/模块只做一件事 |
| 开闭原则 | [solid/ocp/](solid/ocp/) | 扩展开放，修改关闭 |
| 里氏替换原则 | [solid/lsp/](solid/lsp/) | 子类必须能替代父类 |
| 接口隔离原则 | [solid/isp/](solid/isp/) | 客户端不应依赖不需要的接口 |
| 依赖反转原则 | [solid/dip/](solid/dip/) | 高层模块不依赖低层模块 |

### 并发模式 (4)

| 主题 | 目录 | 核心演示 |
|------|------|----------|
| 生产者-消费者 | [concurrency/producer-consumer/](concurrency/producer-consumer/) | 通过队列解耦生产和消费 |
| Reactor | [concurrency/reactor/](concurrency/reactor/) | 单线程事件循环处理多路 I/O |
| 读写锁 | [concurrency/read-write-lock/](concurrency/read-write-lock/) | 读共享、写互斥的并发控制 |
| Future/Promise | [concurrency/future-promise/](concurrency/future-promise/) | 异步操作的占位对象 |

### 反模式 (4)

| 主题 | 目录 | 核心演示 |
|------|------|----------|
| God Object | [anti-patterns/god-object/](anti-patterns/god-object/) | 一个对象承担所有职责 |
| 紧耦合 | [anti-patterns/tight-coupling/](anti-patterns/tight-coupling/) | 模块间直接依赖具体实现 |
| 过早优化 | [anti-patterns/premature-optimization/](anti-patterns/premature-optimization/) | 在不确定瓶颈前就优化 |
| 复制粘贴编程 | [anti-patterns/copy-paste-programming/](anti-patterns/copy-paste-programming/) | 复制代码而非抽象共用逻辑 |

## 代码原则

- 纯 Python 标准库，无需安装额外依赖
- 单文件可运行：`python example.py` 即可看到输出
- 最小化示例：只演示核心机制，通常 < 80 行
- 输出驱动：运行结果清晰展示架构/模式的作用
- 注释解释 why，不只是 what——连接代码与概念

## 贡献

欢迎添加新的架构模式或设计模式主题。每个新主题请遵循已有目录的 README.md 模板和代码原则。完整规划见 [docs/roadmap.md](docs/roadmap.md)。
