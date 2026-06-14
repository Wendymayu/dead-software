# Hadoop MapReduce —— 黑板架构的大规模实践

## 软件简介

Hadoop MapReduce 是由 Doug Cutting 和 Mike Cafarella 在 2006 年基于 Google MapReduce 论文实现的开源分布式数据处理框架。MapReduce 将大规模数据处理分解为两个阶段：Map（将输入数据并行处理为中间结果）和 Reduce（将中间结果聚合为最终输出）。从架构模式角度看，MapReduce 是黑板模式在分布式数据处理领域的经典实践。

## 该软件的架构

MapReduce 的架构可以完美映射到黑板模式的三要素：

- **黑板 = HDFS 中间存储**：Mapper 的输出写入分布式文件系统(HDFS)的中间区域，Reducer 从同一区域读取。HDFS 就是黑板——共享的数据空间，多个专家通过它间接协作。

- **Mapper = 独立专家**：每个 Mapper 是一个独立的"专家"，只处理自己被分配的数据块(chunk)，不关心其他 Mapper 的存在。Mapper 的输出（key-value 对）写入黑板，供 Reducer 读取。Mapper 之间互不通信——这正是黑板模式中"专家独立工作"的原则。

- **Reducer = 聚合专家**：Reducer 从黑板读取所有 Mapper 对同一 key 的输出，进行聚合计算（如求和、计数、最大值），产生最终结果。Reducer 只通过黑板与 Mapper 间接协作——没有直接通信。

- **JobTracker = 控制器**：JobTracker（Hadoop 1.x）或 YARN ResourceManager（Hadoop 2.x）是黑板模式的"控制器"，负责调度 Mapper 和 Reducer 的执行、监控进度、处理故障。

```
输入数据 → [分块] → Mapper-A → 黑板(HDFS) ← Reducer-1 → 最终输出
                    Mapper-B → 黑板(HDFS) ←
                    Mapper-C → 黑板(HDFS) ←
          [JobTracker 控制器调度所有专家]
```

**Shuffle & Sort = 黑板的组织机制**：Mapper 的输出经过 Shuffle & Sort 阶段按 key 排序后传递给 Reducer。这相当于黑板模式中"控制器对黑板数据进行组织"，使 Reducer 能够高效地读取特定 key 的所有值。

## 简化实现思路

本示例模拟 MapReduce 作为黑板模式：

1. **Blackboard**：共享数据空间，存储输入数据块和 Mapper 的中间结果（key → [values]）
2. **MapperExpert**：独立专家，处理分配的数据块，将中间结果写入黑板
3. **ReducerExpert**：聚合专家，从黑板读取所有 key 的中间结果，聚合为最终输出
4. **JobTracker**：控制器，依次调度 Mapper 阶段和 Reducer 阶段

## 与真实实现的对照

| 简化实现 | Hadoop 真实实现 | 差异说明 |
|---------|----------------|---------|
| 内存字典 | HDFS 分布式文件系统 | 真实 Hadoop 的中间数据存储在分布式文件系统 |
| 3个 Mapper | 数百到数千个 Mapper | 真实 Hadoop 可以在数千台机器上并行运行 Mapper |
| 无 Shuffle | Hadoop 有 Shuffle & Sort 阶段 | 真实 MapReduce 中 Mapper 输出经过排序后传给 Reducer |
| 无故障恢复 | Hadoop 有 Task 重试和推测执行 | 真实 Hadoop 自动重试失败的 Task，甚至在慢 Task 上启动备份 |
| 单线程 | 多机多进程并行 | 真实 Mapper 和 Reducer 在不同机器上并行执行 |

**Hadoop 的关键设计决策**：
1. **Mapper 之间零通信**：Mapper 不直接通信，只通过黑板(HDFS)间接协作。这保证了 Mapper 可以独立运行、独立扩展——新增 Mapper 不影响已有 Mapper。
2. **数据本地化**：Hadoop 尽量将 Mapper 分配到存储对应数据块的机器上运行，减少数据传输开销。
3. **推测执行**：如果某个 Mapper 执行特别慢，Hadoop 会在另一台机器上启动相同的 Mapper，先完成的被采纳——这是黑板模式中"控制器优化专家调度"的体现。

## 学习建议

1. **从黑板模式理解 MapReduce**：Mapper 和 Reducer 不是"通信协作"的，而是"通过黑板间接协作"的。这是黑板模式的核心——专家之间不需要直接通信，通过共享数据空间协作。

2. **对比直接通信和黑板协作**：如果 Mapper 和 Reducer 直接通信，你需要设计通信协议、处理消息丢失、管理连接。通过黑板(HDFS)间接协作，这些复杂性全部消失——Mapper 只写，Reducer 只读。

3. **理解 Shuffle 的价值**：Shuffle & Sort 是黑板模式中"控制器组织黑板数据"的体现。没有 Shuffle，Reducer 就要自己从海量中间结果中找到需要的数据——效率极低。Shuffle 将数据按 key 排序，使 Reducer 可以高效读取。

4. **延伸到 Spark**：Apache Spark 是 MapReduce 的进化版。Spark 的 RDD（Resilient Distributed Dataset）可以理解为"更智能的黑板"——支持内存缓存、 lineage（血缘）恢复、更丰富的操作。对比 MapReduce 和 Spark，理解"黑板模式如何在新技术中演进"。

5. **阅读 Google MapReduce 论文**：推荐阅读原始论文 "MapReduce: Simplified Data Processing on Large Clusters"（Dean & Ghemawat, 2004），理解 Google 为什么选择这种架构——大规模数据处理需要"简单、可靠、可扩展"的并行计算模型。
