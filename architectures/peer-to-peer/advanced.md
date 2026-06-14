# BitTorrent：P2P 架构的经典实现

## 软件简介

BitTorrent 是 Bram Cohen 于 2001 年开发的 P2P 文件分发协议。它彻底改变了大文件分发的方式——发布者不需要为每个下载者提供完整带宽，而是利用下载者之间的互相传输来分担负载。一个文件的下载者同时也是上传者，形成自扩展的分发网络。BitTorrent 已成为互联网大文件传输的基础设施。

## 该软件的架构

BitTorrent 的 P2P 架构由三个核心机制组成：

- **Tracker（跟踪器）**：Tracker 是发现协调者，**不传输文件数据**。新 Peer 连接 Tracker，Tracker 返回当前参与下载的其他 Peer 列表和地址。Tracker 只负责"介绍"，数据传输完全在 Peer 之间直接进行。
- **分片直接交换**：文件被分成固定大小的 piece（通常 256KB-1MB），每个 piece 有 SHA1 哈希验证。Peer 之间通过 TCP 直连，互相请求和传输 piece。Peer A 从 Peer B 下载 piece-0 后，Peer A 也成为 piece-0 的提供者，可共享给其他人——"下载即上传"。
- **策略机制**：最稀有优先（Rarest-first）确保稀有分片尽快扩散；互惠上传（Tit-for-tat）激励贡献——优先向给自己上传数据的 Peer 回报。

```
Tracker (发现协调，不传输数据)
  ↓ 返回 Peer 列表和地址
Peer-A ←──TCP直连──→ Peer-B ←──TCP直连──→ Peer-C
  下载 piece-0      上传 piece-0       下载 piece-3
  上传 piece-3      下载 piece-3       上传 piece-0
  (每个 Peer 同时下载和上传多个 piece)
  (Peer A 下载 piece-0 后，也能向 Peer C 上传 piece-0)
```

## 简化实现思路

本示例用 Python 标准库模拟 BitTorrent 的 P2P 机制：

| 简化概念 | 对应 BitTorrent 机制 |
|---------|---------------------|
| `Tracker` TCP 服务器 | BitTorrent Tracker 的 announce 接口 |
| `Peer.announce` 连接 Tracker | 客户端向 Tracker 注册并获取 Peer 列表 |
| `Peer._serve_pieces` TCP 服务器 | BitTorrent Peer 的 piece 服务端口 |
| `Peer.download(piece_id)` | BitTorrent 的 piece 请求和下载 |
| Peer A 下载后可向 Peer C 上传 | BitTorrent "下载即上传"的扩展机制 |

## 与真实实现的对照

| 简化实现 | 真实 BitTorrent |
|---------|----------------|
| Tracker 返回全部 Peer 列表 | 真实 Tracker 返回随机子集，避免信息过载 |
| 请求任意可用分片 | 真实 BitTorrent 用最稀有优先策略选择分片 |
| 简单直接上传 | 真实 BitTorrent 用互惠（tit-for-tat）策略决定向谁上传 |
| 固定 8 分片无验证 | 真实文件可能有数千 piece，每个有 SHA1 哈希验证 |
| 同机器多进程模拟 | 真实 Peer 分布在全球，通过 TCP 直连 |
| 无 choking/unchoking | 真实 BitTorrent 有 choking 策略惩罚不上传的 Peer |
| 无 DHT | 现代 BitTorrent 支持 DHT（分布式哈希表），Trackerless 模式 |

## 学习建议

1. **理解 Tracker 的角色边界**：Tracker 只负责"介绍 Peer"，不传输数据。这是 P2P 的核心设计——**数据传输去中心化，发现服务可以中心化**。思考：如果 Tracker 宕机，网络还能工作吗？（答案：DHT 使得 Trackerless 成为可能）
2. **研究"下载即上传"的扩展性**：Peer A 下载 piece-0 后立即成为 piece-0 的提供者。N 个下载者 = N 个上传者——这是 P2P 的自扩展性。对比：N 个下载者 + 1 个中心服务器 = 服务器带宽瓶颈。
3. **理解最稀有优先策略**：为什么不顺序下载？因为"所有人都在抢同一块"导致稀有分片更稀有。最稀有优先让分片均匀扩散，加快整体完成速度。
4. **理解互惠机制**：Tit-for-tat 是 BitTorrent 的"经济模型"——只给上传者回报，不给"吸血者"传输。思考：这个策略如何防止自私行为？
5. **延伸阅读**：研究 DHT（Kademlia）如何在无 Tracker 的情况下实现 Peer 发现，以及 μTP（Micro Transport Protocol）如何优化 P2P 网络传输。
