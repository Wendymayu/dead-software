# 事件驱动架构进阶：Redis Pub/Sub

## 软件简介

Redis 是最流行的内存数据存储系统，除了缓存和键值存储，它还提供了 Pub/Sub（发布订阅）功能。Redis Pub/Sub 是一种轻量级的事件驱动通信机制：发布者将消息发送到频道，所有订阅该频道的客户端实时收到消息。这种模式广泛应用于实时通知、消息广播、微服务间事件通信等场景。

## 该软件的架构

Redis Pub/Sub 的核心机制：

1. **频道(Channel)**：消息的主题分类
   - 发布者向指定频道发送消息：`PUBLISH news.tech "新框架发布"`
   - 订阅者订阅指定频道：`SUBSCRIBE news.tech`
   - 一个频道可以有多个订阅者，一条消息会被所有订阅者收到

2. **模式订阅(Pattern Subscribe)**：通配符匹配频道名
   - `PSUBSCRIBE news.*` — 匹配所有以 `news.` 开头的频道
   - `PSUBSCRIBE h?llo` — `?` 匹配单个字符
   - 模式订阅者收到消息时会知道实际匹配的频道名

3. **架构特点**：
   - **无持久化**：Pub/Sub 消息不存储，订阅者必须在线才能收到
   - **fire-and-forget**：发布者不关心谁收到了消息
   - **实时性**：消息即时推送，没有队列延迟
   - **解耦**：发布者和订阅者互不感知对方的存在

Redis 5.0 引入了 Streams（持久化消息流），弥补了 Pub/Sub 不持久化的不足。

## 简化实现思路

我们的简化代码模拟了 Redis Pub/Sub 的核心功能：

- `RedisPubSub` 类 → 模拟 Redis 的 Pub/Sub 机制
- `subscribe()` → 对应 Redis 的 `SUBSCRIBE` 命令，精确频道订阅
- `psubscribe()` → 对应 Redis 的 `PSUBSCRIBE` 命令，模式订阅
- `publish()` → 对应 Redis 的 `PUBLISH` 命令，先匹配精确频道再匹配模式
- `_match_pattern()` → 用 `fnmatch` 实现通配符匹配（对应 Redis 的 glob 匹配规则）

数据流：`PUBLISH channel message` → 精确频道订阅者收到 → 模式订阅者收到

## 与真实实现的对照

| 简化代码 | 真实 Redis Pub/Sub | 说明 |
|---------|-------------------|------|
| `subscribe(channel, callback)` | `SUBSCRIBE channel` | 真实Redis是客户端-服务器模型，订阅通过TCP连接 |
| `psubscribe(pattern, callback)` | `PSUBSCRIBE pattern` | 真实Redis支持 `*`、`?`、`[...]` 通配符 |
| `publish(channel, message)` | `PUBLISH channel message` | 真实Redis返回收到消息的订阅者数量 |
| `fnmatch` 匹配 | Redis glob匹配 | 匹配规则一致：`*`任意、`?`单个字符 |
| 内存字典存储频道 | Redis内部数据结构 | 真实Redis用链表+字典维护频道-客户端映射 |
| 无持久化 | Pub/Sub确实不持久化 | 两者一致——这是Pub/Sub的本质特征 |
| 单线程回调 | 多客户端TCP连接 | 真实Redis是多客户端通过网络协议通信 |

## 学习建议

1. **理解 Pub/Sub 本质**：发布者不知道订阅者存在，订阅者也不知道发布者存在——完全解耦
2. **对比 Pub/Sub vs 消息队列**：Pub/Sub 是实时广播（无持久化），消息队列是持久存储（可事后消费）
3. **思考无持久化的影响**：如果订阅者短暂断线，会丢失消息——何时该用 Pub/Sub，何时该用 Stream？
4. **动手实验**：启动 Redis，用 `redis-cli` 执行 `SUBSCRIBE` 和 `PUBLISH`，观察消息如何实时推送
5. **微服务场景**：Pub/Sub 是微服务间事件通知的轻量级方案，适合"广播型"通知，不适合"任务型"分发
