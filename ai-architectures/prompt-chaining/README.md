# Prompt Chaining (提示词链)

## 什么是 Prompt Chaining

Prompt Chaining 将多个提示词串联成链——每步输出作为下步输入，分阶段解决复杂任务。不同于 ReAct 的"边想边做"，Prompt Chaining 是"按预定流程一步步走"。每个提示词只做一件事，输入清晰、输出清晰，最终串联完成整个任务。

## 核心思想

**一个提示词解决不了的任务，拆成多个简单步骤串起来。每步只做一件事，输入清晰、输出清晰。**

```
Prompt Chain：

  原始输入 ──→ Step1 ──→ Step2 ──→ Step3 ──→ ... ──→ 最终输出
                  │          │          │                │
              提取主题    收集资料    撰写大纲          审核优化
                  │          │          │                │
              简单明确    简单明确    简单明确          简单明确

分支链：

  Step1 ──→ 判断类型 ──→ 技术链(Step2a→Step3a→Step4a)
                      ──→ 创意链(Step2b→Step3b→Step4b)

并行链：

  ┌──→ 链A(事实核查) ──→ ┐
  Step1                    Merge ──→ 最终输出
  └──→ B(风格润色) ──→ ┘
```

关键特征：
- **顺序执行** — 步骤按预定顺序依次执行，不跳步不回退
- **单向传递** — 每步输出只流向下一步，不形成循环
- **步骤自治** — 每个步骤独立，只关注自己的输入和输出
- **可检查性** — 中间步骤结果可随时检查和调试

## 代码示例

运行基础示例：

```bash
python example.py
```

关键代码解读：

1. **5个独立步骤** — `extract_topic`、`research`、`write_outline`、`write_content`、`review` 各模拟一个提示词，只做一件事
2. **prompt_chain 函数** — 将5个步骤依次串联：`output = step1(input); output = step2(output); ...`，体现"每步输出作为下步输入"的核心思想
3. **单向传递** — 数据从步骤1流向步骤5，没有循环或回退
4. **中间结果可检查** — 每步打印自己的输入和输出，便于调试和理解链路

每步只做一件事，串联起来完成复杂任务：这就是 Prompt Chaining 的核心。

## 进阶示例

运行进阶示例：

```bash
python advanced.py
```

进阶示例展示两种进阶链结构：

1. **分支链** — 根据中间结果（话题类型）选择不同路径：技术话题走技术链（研究→技术大纲→技术报告），创意话题走创意链（素材→故事框架→叙事散文）
2. **并行链** — 两条链同时处理不同维度（链A做事实核查、链B做风格润色），最终 `merge` 合并结果

分支链体现了"预定流程中的条件判断"，并行链体现了"多维度同时处理后合并"。

## 优缺点

**优点**
- 每步简单可控——单个提示词只做一件事，降低出错概率
- 中间结果可检查——每步输出都可人工审核和调试
- 步骤可复用组合——同一步骤可在不同链中复用
- 质量更稳定——比单次长提示更容易获得高质量结果

**缺点**
- 预定流程缺乏灵活性——无法根据中间结果动态跳步或回退
- 中间步骤错误会传播——某步出错会影响后续所有步骤
- 不适合需要动态决策的任务——决策型任务更适合 ReAct 模式
- 总延迟是所有步骤之和——每步都需要一次 LLM 调用

## 真实项目中的应用

- **Anthropic Prompt Chaining Guide** — Anthropic 官方推荐的提示词链最佳实践，提倡将复杂任务拆成多步
- **LangChain Sequential Chains** — LangChain 的 SequentialChain 实现提示词链顺序执行
- **OpenAI Cookbook Chaining** — OpenAI cookbook 中的提示词组合与链式调用示例
- **文档生成 Pipeline** — 从提取→整理→撰写→审核的文档生成链，广泛应用于技术写作场景

## 进一步阅读

- [Anthropic "Prompt chaining" Guide](https://docs.anthropic.com/en/docs/build-with-claude/prompt-chaining) — Anthropic 官方提示词链指南
- [LangChain Chain Docs](https://python.langchain.com/docs/concepts/chains/) — LangChain 链的概念与实现
- [OpenAI Cookbook "Combining prompts"](https://cookbook.openai.com/articles/related_resources) — OpenAI cookbook 中的提示词组合方法
