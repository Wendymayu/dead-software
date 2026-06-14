# Git —— 事件溯源的教科书级实现

## 软件简介

Git 是由 Linus Torvalds 在 2005 年创建的分布式版本控制系统，用于跟踪文件变更历史、协调多人协作开发。Git 的核心设计思想是：**不存储文件的当前状态，而是存储每一次变更（diff）作为不可变事件**，当前文件内容通过回放事件序列推导得出。这使得 Git 成为事件溯源模式在文件系统领域的教科书级实现。

## 该软件的架构

Git 的架构本质上是事件溯源系统：

- **提交(Commit) = 不可变事件**：每个 commit 记录"发生了什么变更"（diff/tree）、"谁做的"（author）、"什么时候做的"（timestamp），以及"基于哪个事件"（parent）。提交一旦创建就不可修改——这正是事件溯源"事件不可变"的核心原则。

- **checkout = 回放重建状态**：`git checkout <branch>` 的工作原理是从该分支的 HEAD commit 开始，沿 parent 链回溯到初始提交，按时间顺序回放所有 diff，最终重建出当前工作目录的文件内容。这与事件溯源的 `replay(events)` 完全一致。

- **分支(Branch) = 事件流分叉**：创建分支就是在某个 commit 处产生两条并行的事件流——main 分支和 feature 分支各自独立演进，各自追加新事件（commits）。两条流共享相同的历史前缀，但从此分叉。

- **合并(Merge) = 事件流汇聚**：`git merge` 将两条分叉的事件流重新合并为一条。合并 commit 有两个 parent，代表两条事件流的交汇点。

- **日志(Log) = 事件流**：`git log` 显示完整的事件序列，每条事件记录了系统状态的变更历史。

```
main:    C1 → C2 → C3 → C5 (merge)
                       ↗       ↘
feature:        C3 → C4 → C5
```

## 简化实现思路

本示例模拟 Git 的核心事件溯源机制：

1. **Commit 类**：不可变事件，存储 diffs（文件变更）、parent（父事件）、message（描述）
2. **replay()**：从目标 commit 沿 parent 链逆序收集事件，然后按时间顺序回放 diffs 重建文件状态
3. **branch()**：在某个 commit 处创建新的事件流（仅记录 HEAD 位置）
4. **merge()**：将 source 分支的当前状态作为新 commit 的 diffs 合入 target 分支

## 与真实实现的对照

| 简化实现 | Git 真实实现 | 差异说明 |
|---------|------------|---------|
| `diffs` 存储文本变更 | Git 存储完整 tree 对象（blob + tree） | Git 用 content-addressable 存储，diff 通过对比 tree 计算 |
| `replay()` 每次从头回放 | Git checkout 从 commit 的 tree 对象直接重建 | 真实 Git 每个 commit 都保存完整 tree，不需要回放 |
| 合并时直接合并 diffs | Git 使用三路合并算法 | 真实 Git 找到共同祖先(OCA)，基于三路diff智能合并 |
| 无冲突检测 | Git 有冲突检测和手动解决机制 | 真实 Git 当两个分支修改同一文件的同一位置时报告冲突 |
| 单线程本地模拟 | Git 是分布式，每个仓库都有完整事件历史 | 真实 Git 每个克隆都包含完整的 commit 历史（分布式事件存储） |

**关键洞察**：Git 每个 commit 同时保存完整 tree（快照）和 parent 链（事件流），这是事件溯源配合快照优化的典型实践——不需要每次都从头回放，可以从最近的快照开始。

## 学习建议

1. **从 Git 入手理解事件溯源**：Git 是最常见的、开发者每天都在使用的事件溯源系统。理解 Git 的工作原理（commit、checkout、branch、merge）就是理解事件溯源的核心概念。

2. **对比传统 CRUD 和事件溯源**：思考"如果 Git 用 CRUD 方式存储（只保存文件当前状态，每次变更覆盖旧值）"，你会丢失什么？——完整的变更历史、分支能力、回溯能力。

3. **深入阅读 Git 内部机制**：推荐阅读《Pro Git》第10章"Git Internals"，理解 Git 的对象模型（blob、tree、commit、tag），这是事件溯源在文件系统的完整实现。

4. **延伸到业务系统的事件溯源**：将 Git 的概念映射到业务系统：commit = 业务事件（OrderCreated、PaymentCompleted），checkout = 查询当前状态，branch = 业务流程分叉，merge = 合并决策。

5. **实践 EventStoreDB**：Git 是文件系统的事件溯源，EventStoreDB 是业务系统的事件溯源。两者核心机制相同，但面向不同领域。
