# ReAct (Reason+Act) 模式

## 什么是 ReAct

ReAct 让 Agent 在推理(Reason)和行动(Act)之间交替循环。每一步先思考要做什么，再执行一个动作，再观察结果，再思考下一步。这是自主 Agent 的核心推理架构。

## 核心思想

**纯推理容易空想，纯行动容易盲动。ReAct 让思考和行动交替进行，每步行动的结果都反馈到下一步思考中，形成闭环。**

```
ReAct 循环：

  Question ──→ Thought ──→ Action ──→ Observation ──→ Thought ──→ ... ──→ Answer
                  ↑            │            │                │
                  └── 思考 ────┘            └── 结果 ────────┘
                  │            │                              │
              先想再做      有依据地行动                   结果驱动下一步思考
```

关键特征：
- **Thought** — 推理步骤，思考当前观察和下一步行动
- **Action** — 调用工具（搜索、查找、计算等），获取外部信息
- **Observation** — 工具返回的结果，成为下一步推理的输入
- **闭环** — 行动结果反馈到推理，推理指导下一步行动

## 代码示例

运行基础示例：

```bash
python example.py
```

关键代码解读：

1. **两个工具** — `search` 模拟搜索引擎返回信息，`lookup` 在已知上下文中查找术语细节
2. **推理路径** — 预设 `trace` 列表，每一步包含 `(思考, 动作名, 动作参数)`，模拟 LLM 的推理输出
3. **Thought → Action → Observation 循环** — Agent 先思考需要什么信息 → 调用 search 获取 → 观察结果 → 再思考需要更深入信息 → 调用 lookup → 观察结果 → 思考后给出最终答案
4. **answer 动作** — 当 Thought 判断信息足够时，直接输出答案，循环终止

思考指导行动，行动结果驱动下一步思考：这就是 ReAct 的核心闭环。

## 进阶示例

运行进阶示例：

```bash
python advanced.py
```

进阶示例展示 ReAct 的关键优势——失败时可以调整策略：

1. **工具返回空结果** — 第一次 `search("量子计算应用难点")` 查询不在数据库，返回 None
2. **推理调整查询** — Thought 分析失败原因（"查询太宽泛"），改为搜索基础概念 `search("量子计算基础")`
3. **换用不同工具** — 需要深入了解时，从 search 换到 lookup，查找术语"退相干"
4. **最终得出答案** — 基于多次观察积累的信息，给出完整的最终答案

这展示了 ReAct 的核心优势：推理不是一次性规划，而是根据每步行动结果动态调整策略。

## 优缺点

**优点**
- 推理可追溯——每步都有 Thought 记录，便于调试和审计
- 行动有依据——先想再做，不是盲目调用工具
- 可处理复杂多步任务——通过循环逐步积累信息
- 失败时可调整策略——Observation 反馈到 Thought，选择替代方案

**缺点**
- 步数不确定——可能无限循环，需要设置最大步数限制
- 每步都调用 LLM——成本高，延迟大
- 推理质量依赖 LLM 能力——思考步骤可能不准确或遗漏
- 工具描述必须清晰——LLM 需要理解工具用途才能正确选择

## 真实项目中的应用

- **LangChain ReAct Agent** — 最流行的 ReAct 实现，支持多种工具和 LLM
- **AutoGPT** — 自主 Agent，用 ReAct 循环分解目标、执行子任务
- **OpenAI Function Calling + Reasoning** — tool_use 与推理结合，本质上就是 ReAct
- **Claude Tool Use** — Anthropic 的工具调用机制，推理与行动交替执行

## 进一步阅读

- Yao et al. — *ReAct: Synergizing Reasoning and Acting in Language Models* (2022，原论文，提出 ReAct 框架)
- [LangChain Agent 文档](https://python.langchain.com/docs/concepts/agents/) — ReAct Agent 的工业级实现
- [OpenAI Function Calling 指南](https://platform.openai.com/docs/guides/function-calling) — 工具调用与推理结合的实践指南
