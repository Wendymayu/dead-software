# Akka：Actor 架构的经典实现

## 软件简介

Akka 是 Lightbend 于 2009 年发布的 JVM Actor 模型框架，将 Carl Hewitt 1973 年提出的 Actor 理论落地为生产级并发系统。Akka 用 Scala/Java 编写，通过"无共享状态、只通过消息通信"实现了无需锁的并发编程，被广泛用于金融交易平台、实时数据分析、IoT 设备管理等高并发场景。

## 该软件的架构

Akka 的 Actor 架构由四个核心概念 + 监督层级组成：

- **ActorRef（引用）**：对 Actor 的逻辑地址。外部只能通过 ActorRef 发送消息（`tell()`），无法直接访问 Actor 内部状态。这保证了封装性——Actor 是并发世界的"对象"，只能通过消息交互。
- **Mailbox（邮箱）**：每个 Actor 有自己的 FIFO 队列。Actor 逐条处理邮箱中的消息，处理完一条才处理下一条。这意味着单个 Actor 内不需要锁——天然线程安全。
- **ActorSystem（系统容器）**：管理所有 Actor 的生命周期。ActorSystem 创建 Actor、调度消息、处理重启。
- **Supervisor（监督者）**：Akka 的"让它崩溃"（Let it crash）哲学。父 Actor 监督子 Actor，子 Actor 崩溃时，监督者决定重启、停止或恢复。这把错误处理从"到处 try-catch"变为"集中监督策略"。

```
ActorSystem
  ├── SupervisorActor (监督者)
  │     ├── WorkerActor-1 ←── Worker 崩溃 → 监督者重启
  │     ├── WorkerActor-2
  │     ↓
  │   [Mailbox: task, result, failed → 逐条处理]
  │
  └─ Dispatcher (线程池)
     Thread-1: WorkerActor-1 处理 task
     Thread-2: WorkerActor-2 处理 task
     Thread-3: idle (可被其他 Actor 使用)

消息流向: Client → Supervisor → Worker → result → Supervisor
崩溃流向: Worker 崩溃 → 通知 Supervisor → Supervisor 重启 Worker
```

## 简化实现思路

本示例模拟了 Akka Actor 系统的核心机制 + 监督者策略：

| 简化概念 | 对应 Akka 机制 |
|---------|--------------|
| `ActorRef.tell()` | Akka 的异步消息发送（不暴露 Actor 内部） |
| `Actor._mailbox` FIFO 队列 | Akka 的 Mailbox 实现 |
| `SupervisorActor` 监督 Worker | Akka 的 Supervisor Strategy |
| `ActorSystem.restart` | Akka 的"重启策略"（Restart Strategy） |
| Worker 模拟崩溃并通知 Supervisor | Akka Actor 崩溃时的自动监督处理 |
| `system.run()` 调度 | Akka Dispatcher 的消息调度 |

## 与真实实现的对照

| 简化实现 | 真实 Akka |
|---------|----------|
| 同进程同步调度 | 真实 Akka 异步跨线程消息传递 |
| 简单 FIFO 队列 | Akka 支持多种 Mailbox（优先级、有界等） |
| 崩溃通过消息通知 | 真实 Akka 用 Supervision Strategy 自动处理 |
| 无位置透明 | Akka ActorRef 可跨网络（Remote/Cluster） |
| 无 Dispatcher | Akka 有可配置的 Dispatcher 和线程池策略 |
| Python 类模拟 | 真实 Akka 是 JVM 上的 Scala/Java 实现 |
| 无 Futures | Akka 支持 Ask 模式返回 Future/Promise |

## 学习建议

1. **理解"无共享状态"的哲学**：Actor 模型的核心是"无共享状态，只通过消息通信"。对比传统并发（锁、信号量），思考为什么"无共享"从根本上避免了竞态条件——**不需要锁，因为没有共享数据**。
2. **研究监督者策略**：Akka 中 Actor 彂成树状层级，父 Actor 是子 Actor 的监督者。"让它崩溃"哲学认为：与其在每个 Actor 内 try-catch，不如让 Actor 崩溃，由监督者决定重启。这把错误处理从"防御式编程"变为"集中恢复策略"。
3. **理解 ActorRef 的封装**：ActorRef 是 Actor 的"门牌号"——外部只能发消息，不能打电话（直接调用方法）。这是并发编程的封装原则：**暴露地址，隐藏实现**。
4. **对比 Actor 与线程**：1 个线程 = 1 个执行流（重量级，KB 级栈），1 个 Actor = 1 个逻辑实体（轻量级，字节级状态）。Akka 可以在 4 个线程上运行百万级 Actor——因为 Actor 处理完消息就释放线程。
5. **延伸阅读**：研究 Akka Cluster（分布式集群）和 Akka Streams（响应式流处理），看 Actor 模型如何从单机并发扩展到分布式系统。理解位置透明——本地 Actor 和远程 Actor 的代码完全相同。
