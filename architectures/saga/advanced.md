# Temporal.io —— 分布式 Saga 的现代实现

## 软件简介

Temporal.io 是一个开源的分布式工作流编排平台，由 Maxim Fateev 和 Samar Abbas 在 2019 年创建（前身是 Uber 开发的 Cadence）。Temporal 的核心使命是：**让开发者只需要定义"业务流程做什么"和"失败后如何补偿"，Temporal 负责所有的重试、超时、持久化、故障恢复**。这使得分布式 Saga 模式从"需要开发者手动实现的复杂逻辑"变为"平台提供的开箱即用能力"。

## 该软件的架构

Temporal 的架构是 Saga 编排模式的工业化实现：

- **Workflow（工作流）**：开发者定义的业务流程，包含一组有序的活动步骤。Workflow 的代码是**确定性**的——给定相同的输入，Workflow 总是执行相同的步骤序列。Temporal 保证 Workflow 执行的持久性：即使服务器宕机，Workflow 的进度也会恢复。

- **Activity（活动）**：Workflow 中的单个步骤，是可能失败的非确定性操作（如调用外部 API、写入数据库）。每个 Activity 可以配置重试策略（最大重试次数、重试间隔、退避策略）。Activity 失败时，Temporal 自动按策略重试——开发者不需要写任何重试代码。

- **Compensation（补偿）**：当 Activity 在所有重试后仍然失败时，Temporal 触发补偿流程：按照已完成 Activity 的逆序执行每个 Activity 的补偿逻辑。这正是 Saga 模式的核心——"正向执行失败时，逆向补偿已完成的步骤"。

- **持久化执行**：Workflow 的每一步执行状态都持久化到数据库。如果执行 Workflow 的服务器宕机，另一台服务器可以从数据库恢复进度继续执行。这是 Temporal 解决分布式系统"故障恢复"的核心机制。

```
WorkflowExecutor
  Activity 1: 创建订单 ─── 成功 ─── 记录补偿: 取消订单
  Activity 2: 支付扣款 ─── 成功 ─── 记录补偿: 退款
  Activity 3: 库存预留 ─── 失败(重试耗尽) ─── 触发补偿
    ← 补偿: 退款 ← 补偿: 取消订单
```

## 简化实现思路

本示例模拟 Temporal 的核心机制：

1. **Activity**：定义执行逻辑、补偿逻辑、最大重试次数
2. **WorkflowExecutor**：编排器，依次执行 Activity，失败时重试，重试耗尽后逆序补偿
3. **_execute_with_retry()**：模拟 Temporal 的自动重试机制
4. **_compensate_all()**：逆序执行已完成 Activity 的补偿——Saga 的核心

## 与真实实现的对照

| 简化实现 | Temporal 真实实现 | 差异说明 |
|---------|-----------------|---------|
| 简单重试(固定次数) | Temporal 支持指数退避、最大重试间隔、可定制重试策略 | 真实 Temporal 的重试策略非常灵活 |
| 内存执行 | Temporal 持久化到数据库(Cassandra/PostgreSQL) | 真实 Temporal 每步执行状态都持久化，宕机可恢复 |
| 无超时 | Temporal 支持 Activity 超时、Workflow 超时 | 真实 Temporal 可以设置各种超时，防止无限等待 |
| 无并发控制 | Temporal 支持 Workflow 并发限制 | 真实 Temporal 可以限制同一 Workflow 的并发执行数 |
| 同步执行 | Temporal 是异步的，Activity 可以在远程 Worker 上执行 | 真实 Temporal 的 Workflow 和 Activity 可以在不同机器上 |

**Temporal 的关键创新**：
1. **开发者只写业务逻辑**：不需要写重试代码、不需要写故障恢复代码、不需要写分布式协调代码。Temporal 平台处理所有这些。
2. **确定性 Workflow**：Workflow 代码必须是确定性的（不能有随机数、不能有当前时间），这使得 Temporal 可以在宕机后重放 Workflow 代码恢复进度。
3. **可视化监控**：Temporal Web UI 可以看到每个 Workflow 的执行过程、哪个 Activity 成功、哪个失败、补偿执行了哪些步骤。

## 学习建议

1. **从 Saga 模式理解 Temporal**：Temporal 是 Saga 编排模式的平台化实现。先理解 Saga 模式的核心（正向执行 + 逆向补偿），再理解 Temporal 如何将 Saga 从"手动实现"变为"平台能力"。

2. **体验 Temporal 的开发者体验**：在 Temporal 的官方文档中，对比"手动实现 Saga"和"用 Temporal 实现 Saga"的代码量——你会发现 Temporal 让开发者只需要关注业务逻辑，重试和补偿由平台自动处理。

3. **理解持久化执行的价值**：Temporal 最核心的价值不是 Saga，而是"持久化执行"。即使 Workflow 执行过程中服务器宕机，Temporal 也能从数据库恢复进度继续执行。这在分布式系统中是革命性的——开发者不再需要担心"万一服务器宕了怎么办"。

4. **对比 Uber Cadence**：Temporal 的前身是 Uber 开发的 Cadence。了解 Cadence 在 Uber 内部的使用场景（订单流程、资金转账、数据分析pipeline），理解为什么 Uber 需要这样的平台。

5. **延伸到 AWS Step Functions**：AWS Step Functions 是类似的分布式工作流编排服务。对比 Temporal（开源、自托管）和 Step Functions（云服务、托管），理解两种方案的适用场景。
