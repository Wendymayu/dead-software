# Roadmap

已完成和计划中的主题。重要性标记：🔴 核心（必须掌握） / 🟡 重要（值得深入了解） / 🟢 参考（了解即可）

## 架构模式 (Architecture Patterns)

| 主题 | 目录 | 核心演示 | 重要性 | 状态 |
|------|------|----------|--------|------|
| 🔴 分层架构 | `architectures/layered/` | 三层分离（展示层/业务层/数据层） | 核心 | ✅ 已完成 |
| 🔴 事件驱动架构 | `architectures/event-driven/` | 事件总线 + 发布订阅 | 核心 | ✅ 已完成 |
| 🔴 微服务架构 | `architectures/microservices/` | 独立服务通过 HTTP 通信 | 核心 | ✅ 已完成 |
| 🔴 管道架构 | `architectures/pipeline/` | 数据经过多个处理阶段流转 | 核心 | ✅ 已完成 |
| 🔴 单体架构 | `architectures/monolithic/` | 单一应用包含所有功能模块 | 核心 | ✅ 已完成 |
| 🔴 MVC | `architectures/mvc/` | Model-View-Controller 三角分离 | 核心 | ✅ 已完成 |
| 🟡 MVP | `architectures/mvp/` | Model-View-Presenter，View 与 Model 完全隔离 | 重要 | ✅ 已完成 |
| 🔴 MVVM | `architectures/mvvm/` | Model-View-ViewModel，数据绑定驱动视图 | 核心 | ✅ 已完成 |
| 🟡 六边形架构 | `architectures/hexagonal/` | 核心业务通过端口与适配器与外部交互 | 重要 | ✅ 已完成 |
| 🟢 客户端-服务器 | `architectures/client-server/` | 客户端发起请求，服务器响应 | 参考 | ✅ 已完成 |
| 🟡 SOA | `architectures/soa/` | 服务通过标准契约协作，强调复用与治理 | 重要 | ✅ 已完成 |
| 🔴 CQRS | `architectures/cqrs/` | 命令与查询分离，读写模型独立 | 核心 | ✅ 已完成 |
| 🔴 无服务器架构 | `architectures/serverless/` | 函数即服务，按调用计费，无需管理基础设施 | 核心 | ✅ 已完成 |
| 🟡 插件架构 | `architectures/plugin/` | 核心系统通过插件注册表动态加载扩展 | 重要 | ✅ 已完成 |
| 🟡 微内核 | `architectures/microkernel/` | 最小核心 + 可选功能扩展 | 重要 | ✅ 已完成 |
| 🟢 对等网络 | `architectures/peer-to-peer/` | 节点既是客户端又是服务器，无中心 | 参考 | ✅ 已完成 |
| 🟡 Actor 模型 | `architectures/actor/` | 每个 Actor 独立状态+邮箱，通过消息通信 | 重要 | ✅ 已完成 |
| 🔴 事件溯源 | `architectures/event-sourcing/` | 以事件序列替代传统状态存储 | 核心 | ✅ 已完成 |
| 🔴 绞杀者模式 | `architectures/strangler/` | 逐步用新系统替换旧系统，渐进式迁移 | 核心 | ✅ 已完成 |
| 🔴 Saga | `architectures/saga/` | 微服务下的分布式长事务协调 | 核心 | ✅ 已完成 |
| 🟢 黑板架构 | `architectures/blackboard/` | 多个专家协同求解，通过共享黑板交换信息 | 参考 | ✅ 已完成 |
| 🟡 REST 架构 | `architectures/rest/` | 资源 + 统一接口 + 无状态通信 | 重要 | ✅ 已完成 |

## AI & Agent 架构模式

AI 应用和 Agent 系统中常用的架构模式。🔴 标记的主题是当前 Agent 开发者必须掌握的。

| 主题 | 目录 | 核心演示 | 重要性 | 状态 |
|------|------|----------|--------|------|
| 🔴 RAG | `ai-architectures/rag/` | 查询 → 检索外部知识 → 增强生成 | 核心 | ✅ 已完成 |
| 🔴 ReAct | `ai-architectures/react/` | 思考→行动→观察循环，Agent 核心推理架构 | 核心 | ✅ 已完成 |
| 🔴 Tool Use | `ai-architectures/tool-use/` | LLM 选择并调用外部工具/函数 | 核心 | ✅ 已完成 |
| 🟡 Prompt Chaining | `ai-architectures/prompt-chaining/` | 多提示词串联，每步输出作为下步输入 | 重要 | ✅ 已完成 |
| 🟡 Router | `ai-architectures/router/` | 分类意图 → 路由到专门处理器 | 重要 | ✅ 已完成 |
| 🔴 Planning | `ai-architectures/planning/` | Agent 分解目标为子任务、制定计划、逐步执行 | 核心 | ✅ 已完成 |
| 🟡 Reflection | `ai-architectures/reflection/` | Agent 生成后自我审视并迭代改进 | 重要 | ✅ 已完成 |
| 🔴 Multi-Agent | `ai-architectures/multi-agent/` | 多个专长 Agent 协作，分工协商 | 核心 | ✅ 已完成 |
| 🔴 Memory | `ai-architectures/memory/` | 短期对话记忆 + 长期知识存储 + 工作记忆 | 核心 | ✅ 已完成 |
| 🔴 Guardrails | `ai-architectures/guardrails/` | 输入/输出验证层，约束 LLM 行为边界 | 核心 | ✅ 已完成 |
| 🔴 Human-in-the-Loop | `ai-architectures/human-in-the-loop/` | 关键决策点等待人类审批 | 核心 | ✅ 已完成 |
| 🔴 MCP | `ai-architectures/mcp/` | 标准化协议连接 LLM 与外部工具和数据源 | 核心 | ✅ 已完成 |

## 设计模式 (Design Patterns)

| 主题 | 目录 | 核心演示 | 重要性 | 状态 |
|------|------|----------|--------|------|
| 🔴 观察者模式 | `design-patterns/observer/` | 一对多依赖通知 | 核心 | ✅ 已完成 |
| 🔴 策略模式 | `design-patterns/strategy/` | 算法族可互换封装 | 核心 | ✅ 已完成 |
| 🔴 工厂模式 | `design-patterns/factory/` | 对象创建逻辑集中管理 | 核心 | ✅ 已完成 |
| 🔴 装饰器模式 | `design-patterns/decorator/` | 动态给对象添加职责 | 核心 | ✅ 已完成 |
| 🔴 单例模式 | `design-patterns/singleton/` | 全局唯一实例（也必须了解其争议） | 核心 | ✅ 已完成 |
| 🔴 适配器模式 | `design-patterns/adapter/` | 不兼容接口之间的转换桥接 | 核心 | ✅ 已完成 |
| 🔴 命令模式 | `design-patterns/command/` | 将操作封装为对象，支持撤销和排队 | 核心 | ✅ 已完成 |
| 🔴 代理模式 | `design-patterns/proxy/` | 为对象提供替代品以控制访问 | 核心 | ✅ 已完成 |
| 🟡 外观模式 | `design-patterns/facade/` | 为复杂子系统提供简化接口 | 重要 | ✅ 已完成 |
| 🟡 组合模式 | `design-patterns/composite/` | 树形结构的统一处理 | 重要 | ✅ 已完成 |
| 🟢 桥接模式 | `design-patterns/bridge/` | 将抽象与实现分离 | 参考 | ✅ 已完成 |
| 🟡 模板方法 | `design-patterns/template-method/` | 父类定义骨架，子类填充步骤 | 重要 | ✅ 已完成 |
| 🟡 状态模式 | `design-patterns/state/` | 对象行为随内部状态变化 | 重要 | ✅ 已完成 |
| 🟢 迭代器模式 | `design-patterns/iterator/` | 顺序访问集合元素 | 参考 | ✅ 已完成 |
| 🟡 责任链模式 | `design-patterns/chain-of-responsibility/` | 请求沿处理链传递 | 重要 | ✅ 已完成 |

## SOLID 原则

设计模式的理论基础，理解这些原则才能真正理解为什么模式这样设计。

| 主题 | 目录 | 核心演示 | 重要性 | 状态 |
|------|------|----------|--------|------|
| 🔴 单一职责原则 | `solid/srp/` | 一个类/模块只做一件事 | 核心 | ✅ 已完成 |
| 🔴 开闭原则 | `solid/ocp/` | 扩展开放，修改关闭 | 核心 | ✅ 已完成 |
| 🟡 里氏替换原则 | `solid/lsp/` | 子类必须能替代父类 | 重要 | ✅ 已完成 |
| 🟡 接口隔离原则 | `solid/isp/` | 客户端不应依赖不需要的接口 | 重要 | ✅ 已完成 |
| 🔴 依赖反转原则 | `solid/dip/` | 高层模块不依赖低层模块 | 核心 | ✅ 已完成 |

## 并发模式 (Concurrency Patterns)

后端和高性能场景的核心知识，AI Agent 的异步执行也依赖这些模式。

| 主题 | 目录 | 核心演示 | 重要性 | 状态 |
|------|------|----------|--------|------|
| 🔴 生产者-消费者 | `concurrency/producer-consumer/` | 通过队列解耦生产和消费 | 核心 | ✅ 已完成 |
| 🟡 Reactor 模式 | `concurrency/reactor/` | 单线程事件循环处理多路 I/O | 重要 | ✅ 已完成 |
| 🟡 读写锁 | `concurrency/read-write-lock/` | 读共享、写互斥的并发控制 | 重要 | ✅ 已完成 |
| 🔴 Future/Promise | `concurrency/future-promise/` | 异步操作的占位对象 | 核心 | ✅ 已完成 |

## 反模式 (Anti-Patterns)

知道什么是错的，比知道什么是对的更能防止犯错。

| 主题 | 目录 | 核心演示 | 重要性 | 状态 |
|------|------|----------|--------|------|
| 🔴 God Object | `anti-patterns/god-object/` | 一个对象承担所有职责 | 核心 | ✅ 已完成 |
| 🔴 紧耦合 | `anti-patterns/tight-coupling/` | 模块间直接依赖具体实现 | 核心 | ✅ 已完成 |
| 🟡 过早优化 | `anti-patterns/premature-optimization/` | 在不确定瓶颈前就优化 | 重要 | ✅ 已完成 |
| 🔴 复制粘贴编程 | `anti-patterns/copy-paste-programming/` | 复制代码而非抽象共用逻辑 | 核心 | ✅ 已完成 |

---

## 跨主题关联

以下主题之间存在强关联，阅读顺序会影响理解效果：

- 单体架构 → 分层架构 → 六边形架构 → 微服务架构（系统的演化路径）
- 单体架构 → 绞杀者模式 → 微服务架构（渐进迁移路径）
- 客户端-服务器 → SOA → 微服务架构 → 无服务器架构（分布式架构的演进）
- MVC → MVP → MVVM（展示层架构的三代演进）
- 插件架构 → 微内核（扩展机制从粗粒度到细粒度）
- 管道架构 → Prompt Chaining（传统数据管道 → LLM 提示词管道）
- 观察者模式 → 事件驱动架构 → 事件溯源 → CQRS（从微观到宏观）
- Actor 模型 → 事件驱动架构（两种并发通信范式）
- 策略模式 → 命令模式 → 责任链模式（行为型模式的演进）
- 装饰器模式 → 代理模式 → 适配器模式（结构型包装模式的对比）
- 工厂模式 → Tool Use（对象创建 → 工具调用，都是"按需获取能力"）
- 责任链模式 → Router → Guardrails（请求逐层过滤/路由/校验）
- 观察者模式 → Memory（状态变化 → 记忆更新与召回）
- ReAct → Reflection → Planning（单步推理 → 自我审视 → 多步规划，Agent 能力递进）
- 黑板架构 → Multi-Agent（共享空间协同 → 多 Agent 协商）
- 六边形架构 → MCP（端口与适配器 → 标准化工具协议，都是"核心与外部解耦"）
- Human-in-the-Loop → Guardrails（人为介入 → 自动约束，两种 AI 安全策略）
- 管道架构 → 生产者-消费者 → Reactor（管道的并发变体）
- SOLID 原则 → 设计模式 → 架构模式（理论 → 微观 → 宏观）

---

## 贡献指南

添加新主题时：

1. 在此 roadmap 中标注状态为 🔄 进行中
2. 遵循已有目录的 README.md 模板和代码原则
3. 完成后运行 `python shared/verify_all.py` 确认所有示例正常
4. 更新项目根目录 README.md 的导航索引
5. 提交后将状态更新为 ✅ 已完成
