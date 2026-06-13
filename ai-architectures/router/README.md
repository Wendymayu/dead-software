# Router (路由分发)

## 什么是 Router

Router 分类用户意图后路由到专门处理器/Agent。避免一个大模型包打天下，不同意图交给不同专长处理。

核心流程：**用户查询 → 意图分类 → 路由到处理器 → 专门处理 → 返回结果**

## 核心思想

**分类再分发——先搞清楚用户要什么，再交给最擅长处理这类请求的专家。就像客服热线——先听你说什么，再转接到对应部门。**

```
Router 分发流程：

  User Query ──→ Classifier ──→ Handler A (代码问题)
                      │         → Handler B (数学问题)
                      │         → Handler C (创意请求)
                      │         → General    (兜底处理)
                      │
                 意图分类         各处理器专注单一领域
                 确定路由         路由后处理更精确
```

关键特征：
- **Classifier** — 分析用户查询，输出意图类别和置信度
- **Handler** — 每个处理器专注单一领域，处理逻辑专精
- **路由分发** — 根据分类结果将请求转发到匹配处理器
- **回退兜底** — 置信度不足时回退到通用处理器，避免错误路由

## 代码示例

运行基础示例：

```bash
python example.py
```

关键代码解读：

1. **四个处理器** — `code_handler`、`math_handler`、`creative_handler`、`general_handler`，各自专注不同领域，处理逻辑独立
2. **意图分类** — `classify_intent` 根据关键词模拟 LLM 意图识别，判断查询属于哪类意图
3. **路由映射** — `INTENT_MAP` 将意图类别映射到对应处理器，分类结果决定分发路径
4. **兜底处理** — 无法匹配特定意图时默认路由到 `general_handler`，保证所有请求都有响应

分类确定路由，路由到达专家——这就是 Router 的核心分发机制。

## 进阶示例

运行进阶示例：

```bash
python advanced.py
```

进阶示例展示两个关键机制：

1. **置信度回退** — `classify_with_confidence` 输出意图和置信度，置信度低于阈值时回退到 `general_handler`，避免低质量分类导致的错误路由
2. **嵌套路由** — 代码问题路由到 `code_router` 后，内部再根据语言关键词二次分类到 `python_handler` 或 `js_handler`，实现多层精准分发

这展示了 Router 的进阶能力：不是简单的一步分发，而是置信度保障 + 多层路由的精准分发体系。

## 优缺点

**优点**
- 每个处理器专注单一领域——处理逻辑专精，输出质量更高
- 路由后处理更精确——专长匹配比通用处理更准确
- 可独立优化每个处理器——升级某领域不影响其他处理器
- 降低单模型负载——不同意图分散到不同处理器，成本可控

**缺点**
- 路由分类可能错误——意图识别不准时会把请求送到错误处理器
- 需要维护多个处理器——每个处理器独立维护，运维成本增加
- 边界模糊的意图难以分类——跨领域查询可能导致路由犹豫
- 增加系统复杂度——分类+分发+回退机制使架构更复杂

## 真实项目中的应用

- **Semantic Router** — 基于语义相似度的意图路由库，用 embedding 匹配路由到对应处理链
- **LangChain Router Chains** — 支持多链路由的 LangChain 组件，根据意图选择不同处理链
- **OpenAI Swarm** — 多 Agent 协作框架，Router 决定请求转发到哪个 Agent
- **各客服系统意图分类** — 工业客服系统先分类意图再转接部门，本质就是 Router

## 进一步阅读

- [Semantic Router 文档](https://github.com/aurelio-labs/semantic-router) — 基于语义相似度的路由库，用 embedding 实现意图匹配
- [LangChain Router 文档](https://python.langchain.com/docs/concepts/routers/) — LangChain 的路由链机制和多链分发实现
- Chen et al. — *FrugalGPT: How to Use Large Language Models with Lower Cost and Higher Quality* (2023，成本感知路由，根据任务难度选择不同级别模型)
