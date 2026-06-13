# Roadmap

已完成和计划中的主题。

## 架构模式 (Architecture Patterns)

| 主题 | 目录 | 核心演示 | 状态 |
|------|------|----------|------|
| 分层架构 | `architectures/layered/` | 三层分离（展示层/业务层/数据层） | ✅ 已完成 |
| 事件驱动架构 | `architectures/event-driven/` | 事件总线 + 发布订阅 | ✅ 已完成 |
| 微服务架构 | `architectures/microservices/` | 独立服务通过 HTTP 通信 | ✅ 已完成 |
| 管道架构 | `architectures/pipeline/` | 数据经过多个处理阶段流转 | ✅ 已完成 |
| 单体架构 | `architectures/monolithic/` | 单一应用包含所有功能模块 | ❌ 未完成 |
| 六边形架构 | `architectures/hexagonal/` | 核心业务通过端口与适配器与外部交互 | ❌ 未完成 |
| CQRS | `architectures/cqrs/` | 命令与查询分离，读写模型独立 | ❌ 未完成 |
| 插件架构 | `architectures/plugin/` | 核心系统通过插件注册表动态加载扩展 | ❌ 未完成 |
| 事件溯源 | `architectures/event-sourcing/` | 以事件序列替代传统状态存储 | ❌ 未完成 |
| REST 架构 | `architectures/rest/` | 资源 + 统一接口 + 无状态通信 | ❌ 未完成 |

## 设计模式 (Design Patterns)

| 主题 | 目录 | 核心演示 | 状态 |
|------|------|----------|------|
| 观察者模式 | `design-patterns/observer/` | 一对多依赖通知 | ✅ 已完成 |
| 策略模式 | `design-patterns/strategy/` | 算法族可互换封装 | ✅ 已完成 |
| 工厂模式 | `design-patterns/factory/` | 对象创建逻辑集中管理 | ✅ 已完成 |
| 装饰器模式 | `design-patterns/decorator/` | 动态给对象添加职责 | ✅ 已完成 |
| 单例模式 | `design-patterns/singleton/` | 全局唯一实例的创建与访问 | ❌ 未完成 |
| 适配器模式 | `design-patterns/adapter/` | 不兼容接口之间的转换桥接 | ❌ 未完成 |
| 命令模式 | `design-patterns/command/` | 将操作封装为对象，支持撤销和排队 | ❌ 未完成 |
| 代理模式 | `design-patterns/proxy/` | 为对象提供替代品以控制访问 | ❌ 未完成 |
| 外观模式 | `design-patterns/facade/` | 为复杂子系统提供简化接口 | ❌ 未完成 |
| 组合模式 | `design-patterns/composite/` | 树形结构的统一处理 | ❌ 未完成 |
| 桥接模式 | `design-patterns/bridge/` | 将抽象与实现分离，使两者独立变化 | ❌ 未完成 |
| 模板方法 | `design-patterns/template-method/` | 父类定义骨架，子类填充步骤 | ❌ 未完成 |
| 状态模式 | `design-patterns/state/` | 对象行为随内部状态变化 | ❌ 未完成 |
| 迭代器模式 | `design-patterns/iterator/` | 顺序访问集合元素而不暴露内部 | ❌ 未完成 |
| 责任链模式 | `design-patterns/chain-of-responsibility/` | 请求沿处理链传递，直到被处理 | ❌ 未完成 |

## SOLID 原则

| 主题 | 目录 | 核心演示 | 状态 |
|------|------|----------|------|
| 单一职责原则 | `solid/srp/` | 一个类/模块只做一件事 | ❌ 未完成 |
| 开闭原则 | `solid/ocp/` | 扩展开放，修改关闭 | ❌ 未完成 |
| 里氏替换原则 | `solid/lsp/` | 子类必须能替代父类 | ❌ 未完成 |
| 接口隔离原则 | `solid/isp/` | 客户端不应依赖不需要的接口 | ❌ 未完成 |
| 依赖反转原则 | `solid/dip/` | 高层模块不依赖低层模块 | ❌ 未完成 |

## 并发模式 (Concurrency Patterns)

| 主题 | 目录 | 核心演示 | 状态 |
|------|------|----------|------|
| 生产者-消费者 | `concurrency/producer-consumer/` | 通过队列解耦生产和消费 | ❌ 未完成 |
| Reactor 模式 | `concurrency/reactor/` | 单线程事件循环处理多路 I/O | ❌ 未完成 |
| 读写锁 | `concurrency/read-write-lock/` | 读共享、写互斥的并发控制 | ❌ 未完成 |
| Future/Promise | `concurrency/future-promise/` | 异步操作的占位对象 | ❌ 未完成 |

## 反模式 (Anti-Patterns)

| 主题 | 目录 | 核心演示 | 状态 |
|------|------|----------|------|
| God Object | `anti-patterns/god-object/` | 一个对象承担所有职责 | ❌ 未完成 |
| 紧耦合 | `anti-patterns/tight-coupling/` | 模块间直接依赖具体实现 | ❌ 未完成 |
| 过早优化 | `anti-patterns/premature-optimization/` | 在不确定瓶颈前就优化 | ❌ 未完成 |
| 复制粘贴编程 | `anti-patterns/copy-paste-programming/` | 复制代码而非抽象共用逻辑 | ❌ 未完成 |

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

1. 在此 roadmap 中标注状态为 🔄 进行中
2. 遵循已有目录的 README.md 模板和代码原则
3. 完成后运行 `python shared/verify_all.py` 确认所有示例正常
4. 更新项目根目录 README.md 的导航索引
5. 提交后将状态更新为 ✅ 已完成
