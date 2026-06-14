# Redis：客户端-服务器架构的经典实现

## 软件简介

Redis（Remote Dictionary Server）是 Salvatore Sanfilippo 于 2009 年开发的内存键值数据存储。它以极高读写性能著称，单线程即可达到 10 万+ QPS。Redis 支持 strings、hashes、lists、sets 等数据结构，并提供持久化、复制、集群等生产级特性，广泛用于缓存、消息队列、会话存储。

## 该软件的架构

Redis 采用**单线程事件循环**的客户端-服务器架构，核心机制如下：

- **单线程事件循环**：Redis 用 `epoll`/`kqueue` 实现 I/O 多路复用（Reactor 模式），在单线程内顺序处理所有客户端请求。内存操作极快（微秒级），单线程避免了锁和竞态条件，反而比多线程更快。
- **RESP 协议**：客户端通过 TCP 连接 Redis，使用 Redis Serialization Protocol（RESP）通信。RESP 是极简文本协议，命令如 `SET key value`，响应如 `OK` 或 `(nil)`。
- **命令处理管线**：客户端发送命令 → 服务器解析 → 执行器执行 → 返回响应。整个过程在一个事件循环迭代中完成。
- **Pub/Sub 模式**：客户端可 SUBSCRIBE 频道，其他客户端 PUBLISH 消息时，服务器推送给所有订阅者。这是 Redis 的消息通信机制。

```
Client-A ──TCP──→ ┌────────────────────────────┐ ──TCP──→ Client-C (订阅者)
Client-B ──TCP──→ │  Event Loop (epoll/kqueue)  │ ←──推送── PUB news
                   │    ↓ Command Parser          │
                   │    ↓ Executor (单线程)        │
                   │    ↓ Data Store (内存)        │
                   │    ↓ Response Writer          │
                   └────────────────────────────┘
                         ↓ RDB/AOF 持久化
```

## 简化实现思路

本示例用 Python 标准库模拟 Redis 的客户端-服务器通信：

| 简化概念 | 对应 Redis 机制 |
|---------|---------------|
| `socketserver.ThreadingTCPServer` | Redis 的 TCP 监听 + 事件循环 |
| `RedisHandler._process` | Redis 的命令解析与执行 |
| `RedisHandler.STORE` 类属性 | Redis 内存中的键值数据 |
| `RedisHandler.SUBS` + PUBLISH | Redis 的 Pub/Sub 机制 |
| `RedisClient.send/recv` | RESP 协议的请求-响应 |
| 多个 Client 连接同一 Server | Redis 多客户端并发连接 |

## 与真实实现的对照

| 简化实现 | 真实 Redis |
|---------|-----------|
| 每连接一个线程处理 | 真实 Redis 单线程事件循环 + I/O 多路复用 |
| 空格分隔的文本命令 | 真实 Redis 用 RESP 二进制协议（更高效） |
| 简单字典存储 | Redis 支持 6 种数据结构 + 过期 + 内存淘汰策略 |
| 无持久化 | Redis 有 RDB 快照和 AOF 日志两种持久化 |
| SUBSCRIBE 无实时推送接收 | 真实 Redis 客户端持续监听订阅推送 |
| 无连接管理 | 真实 Redis 有客户端列表、超时、maxclients |

## 学习建议

1. **阅读 RESP 协议**：理解 Redis 客户端-服务器通信的基础格式。RESP 的极简设计是协议设计的典范——5 种类型前缀（`+`、`-`、`:`、`$`、`*`）覆盖所有场景。
2. **理解单线程的权衡**：Redis 单线程不是因为"能力不足"，而是因为内存操作本身就极快，多线程的锁开销反而拖慢。思考：什么场景下单线程不够用？（答案：网络 I/O 是瓶颈，Redis 6.0+ 用多 I/O 线程处理网络读写）。
3. **研究 epoll/kqueue**：Redis 的性能核心是操作系统提供的高效 I/O 多路复用，这是 Reactor 模式的基础。理解为什么 `select` 不够用，`epoll` 如何做到 O(1) 就绪检测。
4. **理解 Pub/Sub 的局限**：Redis Pub/Sub 是"发后即忘"——订阅者离线时消息丢失。对比 Redis Streams（持久化消息队列），理解不同通信模型的适用场景。
5. **延伸阅读**：研究 Redis Cluster 如何在分布式环境下保持客户端-服务器模型，以及 Redis 7.0 的 Function 特性如何扩展命令处理。
