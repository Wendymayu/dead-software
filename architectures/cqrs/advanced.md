# Axon Framework：CQRS + Event Sourcing 的经典实现

## 软件简介

Axon Framework 是荷兰公司 AxonIQ 于 2010 年发布的 Java 框架，它将 CQRS（命令查询职责分离）和 Event Sourcing（事件溯源）两大架构模式落地为生产级框架。Axon 提供了 CommandBus、QueryBus、EventStore、Projection 等核心组件，让开发者无需自行实现 CQRS 的基础设施。Axon 被广泛用于金融、电商、物流等需要高一致性 + 高性能查询的场景。

## 该软件的架构

Axon Framework 的 CQRS+ES 架构由五大核心组件组成：

- **CommandBus（命令总线）**：所有写操作以 Command 对象的形式提交到 CommandBus。CommandBus 根据 Command 类型路由到对应的 CommandHandler。Command 是意图的表达（如 CreateOrderCommand），不是状态变更的描述——它说"我想要做什么"，而不是"数据变成了什么"。
- **CommandHandler（命令处理器）**：接收 Command，执行业务验证，决定生成哪些 Event。CommandHandler 不直接修改数据库——它只"决定"事件。验证失败时拒绝 Command（抛异常或返回 null）。
- **EventStore（事件存储）**：所有事件以 append-only 方式持久化。EventStore 是 Axon 的核心——它不存储"当前状态"，而是存储"所有变更历史"。任何时刻的状态都可以从事件流重新计算（事件溯源）。
- **EventHandler → Projection（事件处理器 → 投影）**：EventHandler 监听事件，更新 Projection（读模型）。Projection 是为查询优化的数据视图——可以是一张数据库表、一个缓存、一个搜索引擎索引。Projection 随时可以从事件流重建，损坏后零数据丢失。
- **QueryBus（查询总线）**：所有读操作以 Query 对象的形式提交到 QueryBus。QueryBus 路由到 QueryHandler，QueryHandler 查询 Projection 返回结果。Query 和 Command 完全分离——写端和读端可以独立优化、独立扩展。

```
命令流（写端）:
  CreateOrderCommand → CommandBus → CommandHandler → 验证 + 生成事件
    → EventStore (append-only 存储)

事件流（投影更新）:
  EventStore → EventHandler → Projection (更新读模型)

查询流（读端）:
  QueryOrderList → QueryBus → QueryHandler → 查询 Projection → 返回结果

完整链路:
  Command → CommandHandler → Event → EventStore → EventHandler → Projection → QueryHandler
```

## 简化实现思路

本示例模拟了 Axon Framework CQRS 的核心流程：

| 简化概念 | 对应 Axon 机制 |
|---------|--------------|
| `CommandBus.dispatch()` | Axon CommandBus 的命令分发 |
| `CommandBus.register()` | Axon @CommandHandler 注解标记处理器 |
| `QueryBus.dispatch()` | Axon QueryBus 的查询分发 |
| `EventStore.append()` | Axon EventStore 的 append-only 事件存储 |
| `Projection.rebuild()` | Axon Projection 从事件流重建读模型 |
| 命令/查询分离 | Axon CQRS 的核心理念：写端和读端完全分离 |

## 与真实实现的对照

| 简化实现 | 真实 Axon Framework |
|---------|-------------------|
| 简单字典路由 | Axon 使用注解（@CommandHandler/@QueryHandler）+ 反射路由 |
| 内存字典存储 | Axon EventStore 使用 AxonDB（专用事件存储）或 JDBC |
| 同步处理 | Axon 支持异步 CommandBus（DisruptorCommandBus） |
| 单投影 | Axon 支持多个 Projection，每个可以为不同查询优化 |
| 无 Saga | Axon 提供 Saga（流程管理器）协调跨聚合的长时间流程 |
| 无分布式 | Axon Server 提供分布式 EventStore 和 CommandBus |
| 无 Snapshot | Axon 支持快照——聚合事件太多时，定期保存状态快照 |

## 学习建议

1. **理解 CQRS 的分离逻辑**：CQRS 不是"用两个数据库"这么简单——它是对写模型和读模型的根本性分离。写模型关注一致性（Command 验证、Event 确保状态正确），读模型关注查询性能（Projection 可以自由优化索引、分表）。理解"一致性"和"查询性能"的矛盾如何被 CQRS 解决。
2. **理解 Event Sourcing 的价值**：ES 不存储"当前状态"，而是存储"所有变更历史"。这意味着：(1) 任何时刻的状态可以重新计算；(2) 数据损坏可以从事件重建；(3) 可以"时间旅行"——查看任意历史时刻的状态。理解这些优势以及 ES 的代价（事件量大、重建耗时）。
3. **理解 Projection 的自由度**：Projection 是为查询优化的视图——可以有多个 Projection，每个服务于不同的查询需求。一个用数据库表（快速 SQL 查询），一个用 Elasticsearch（全文搜索），一个用 Redis（缓存）。它们都从同一个事件流重建，但物理存储完全不同。
4. **延伸阅读**：研究 Axon Framework 的 Saga（流程管理器）——当业务流程涉及多个聚合（如订单→支付→发货）时，Saga 协调跨聚合的事件流转。这是 CQRS+ES 在复杂业务场景下的关键扩展。
