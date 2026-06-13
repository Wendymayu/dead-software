# Roadmap

已完成和计划中的主题规划。优先级按 P0（首批补充）→ P1（标准扩展）→ P2（进阶扩展）排列。

## 已完成 ✅

### 架构模式 (Architecture Patterns)

| 主题 | 目录 | 状态 |
|------|------|------|
| 分层架构 | `architectures/layered/` | ✅ 已完成 |
| 事件驱动架构 | `architectures/event-driven/` | ✅ 已完成 |
| 微服务架构 | `architectures/microservices/` | ✅ 已完成 |
| 管道架构 | `architectures/pipeline/` | ✅ 已完成 |

### 设计模式 (Design Patterns)

| 主题 | 目录 | 状态 |
|------|------|------|
| 观察者模式 | `design-patterns/observer/` | ✅ 已完成 |
| 策略模式 | `design-patterns/strategy/` | ✅ 已完成 |
| 工厂模式 | `design-patterns/factory/` | ✅ 已完成 |
| 装饰器模式 | `design-patterns/decorator/` | ✅ 已完成 |

---

## P0 — 首批补充

补全最常见的架构和设计模式，让覆盖面更完整。

### 架构模式

| 主题 | 目录 | 核心演示 | 理由 |
|------|------|----------|------|
| 单体架构 | `architectures/monolithic/` | 单一应用包含所有功能模块 | 所有系统的起点，与微服务对比理解 |
| CQRS | `architectures/cqrs/` | 命令与查询分离，读写模型独立 | 事件驱动架构的自然延伸 |
| 六边形架构 | `architectures/hexagonal/` | 核心业务通过端口与适配器与外部交互 | 分层架构的进阶版，依赖反转的实践 |
| 插件架构 | `architectures/plugin/` | 核心系统通过插件注册表动态加载扩展 | 可扩展系统的经典方案 |

### 设计模式

| 主题 | 目录 | 核心演示 | 理由 |
|------|------|----------|------|
| 单例模式 | `design-patterns/singleton/` | 全局唯一实例的创建与访问 | 最常见也最容易误用的模式，值得讨论 |
| 适配器模式 | `design-patterns/adapter/` | 不兼容接口之间的转换桥接 | 系统集成时不可避免 |
| 命令模式 | `design-patterns/command/` | 将操作封装为对象，支持撤销和排队 | 与事件驱动和 CQRS 紧密关联 |
| 代理模式 | `design-patterns/proxy/` | 为对象提供替代品以控制访问 | 微服务中的远程代理、缓存代理的底层原理 |

---

## P1 — 标准扩展

覆盖更多经典模式和重要概念。

### 架构模式

| 主题 | 目录 | 核心演示 | 理由 |
|------|------|----------|------|
| 空间驱动架构 | `architectures/space-driven/` | 基于副本空间的分布式架构 | 与微服务互补的分布式方案 |
| 事件溯源 | `architectures/event-sourcing/` | 以事件序列替代传统状态存储 | CQRS 的配套模式，理解事件驱动的深层机制 |
| REST 架构 | `architectures/rest/` | 资源 + 统一接口 + 无状态通信 | Web 开发的基础架构约束 |

### 设计模式 — 结构型

| 主题 | 目录 | 核心演示 | 理由 |
|------|------|----------|------|
| 外观模式 | `design-patterns/facade/` | 为复杂子系统提供简化接口 | 实际项目中最常用的简化手段 |
| 组合模式 | `design-patterns/composite/` | 树形结构的统一处理 | UI 组件、文件系统的基础模式 |
| 桥接模式 | `design-patterns/bridge/` | 将抽象与实现分离，使两者独立变化 | 与策略模式对比理解 |

### 设计模式 — 行为型

| 主题 | 目录 | 核心演示 | 理由 |
|------|------|----------|------|
| 模板方法 | `design-patterns/template-method/` | 父类定义骨架，子类填充步骤 | 继承式复用的经典案例 |
| 状态模式 | `design-patterns/state/` | 对象行为随内部状态变化 | 消除状态判断的 if/else |
| 迭代器模式 | `design-patterns/iterator/` | 顺序访问集合元素而不暴露内部 | Python 内置迭代器的底层原理 |
| 责任链模式 | `design-patterns/chain-of-responsibility/` | 请求沿处理链传递，直到被处理 | 与管道架构的微观对照 |

---

## P2 — 进阶扩展

更深层或更专题性的内容，按需求逐步添加。

### 新类别：SOLID 原则

| 主题 | 目录 | 核心演示 | 理由 |
|------|------|----------|------|
| 单一职责原则 | `solid/srp/` | 一个类/模块只做一件事 | 设计模式的理论基础 |
| 开闭原则 | `solid/ocp/` | 扩展开放，修改关闭 | 策略/观察者/装饰器都遵循此原则 |
| 里氏替换原则 | `solid/lsp/` | 子类必须能替代父类 | 继承的正确用法 |
| 接口隔离原则 | `solid/isp/` | 客户端不应依赖不需要的接口 | 适配器模式的理论基础 |
| 依赖反转原则 | `solid/dip/` | 高层模块不依赖低层模块 | 已在分层架构进阶示例中演示，独立主题可深入 |

### 新类别：并发模式

| 主题 | 目录 | 核心演示 | 理由 |
|------|------|----------|------|
| 生产者-消费者 | `concurrency/producer-consumer/` | 通过队列解耦生产和消费 | 管道架构和事件驱动的并发版 |
| Reactor 模式 | `concurrency/reactor/` | 单线程事件循环处理多路 I/O | Node.js / Nginx 的核心模型 |
| 读写锁 | `concurrency/read-write-lock/` | 读共享、写互斥的并发控制 | 数据库、缓存系统的基本机制 |
| Future/Promise | `concurrency/future-promise/` | 异步操作的占位对象 | asyncio 的核心抽象 |

### 新类别：反模式

| 主题 | 目录 | 核心演示 | 理由 |
|------|------|----------|------|
| God Object | `anti-patterns/god-object/` | 一个对象承担所有职责 | SRP 的反面教材 |
| 紧耦合 | `anti-patterns/tight-coupling/` | 模块间直接依赖具体实现 | 依赖反转的反面教材 |
| 过早优化 | `anti-patterns/premature-optimization/` | 在不确定瓶颈前就优化 | 性能工程的基本陷阱 |
| 复制粘贴编程 | `anti-patterns/copy-paste-programming/` | 复制代码而非抽象共用逻辑 | 维护性的根本敌人 |

---

## 跨主题关联

以下主题之间存在强关联，阅读顺序会影响理解效果：

- 分层架构 → 六边形架构 → 微服务架构（从简单到复杂，层层递进）
- 观察者模式 → 事件驱动架构 → 事件溯源 → CQRS（从微观到宏观）
- 策略模式 → 命令模式 → 责任链模式（行为型模式的演进）
- 装饰器模式 → 代理模式 → 适配器模式（结构型包装模式的对比）
- 管道架构 → 生产者-消费者 → Reactor（管道的并发变体）
- SOLID 原则 → 设计模式 → 架构模式（理论 → 微观 → 宏观）

---

## 贡献指南

添加新主题时：

1. 在此 roadmap 中找到对应位置，标注状态为 🔄 进行中
2. 遵循已有目录的 README.md 模板和代码原则
3. 完成后运行 `python shared/verify_all.py` 确认所有示例正常
4. 更新项目根目录 README.md 的导航索引
5. 提交后将 roadmap 中状态更新为 ✅ 已完成
