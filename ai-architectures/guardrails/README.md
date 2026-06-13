# Guardrails（护栏）架构

## 什么是 Guardrails

Guardrails 是约束 LLM 行为的验证层——输入验证（拒绝不当查询）、输出验证（检查安全性和格式）、流程约束（执行中强制业务规则）。它们是 LLM 和真实世界之间的安全网。

## 核心思想

**LLM 是不可控的——它可能输出有害内容、泄露隐私、违反业务规则。Guardrails 在 LLM 的"前面"（输入）和"后面"（输出）设置关卡，确保行为在安全边界内。**

```
Guardrails 验证链路：

  用户查询 ──→ [InputGuard] ──→ LLM ──→ [OutputGuard] ──→ [BusinessGuard] ──→ 用户
                  │                        │                     │
                拦截不当输入             检查格式与安全         强制业务规则
                  │                        │                     │
                ✗ 拒绝               ✗ 拦截 / 脱敏          ✗ 拦截 / 脱敏
                  ↓                        ↓                     ↓
              返回拒绝理由            记录日志 + 阻断       记录日志 + 阻断
```

关键特征：
- **InputGuard** — 在 LLM 处理前拦截不当查询，拒绝有害/非法请求
- **OutputGuard** — 在 LLM 输出后检查安全性、格式合规性
- **BusinessGuard** — 强制业务规则，如禁止泄露内部定价、强制特定字段
- **失败策略** — log（记录）、block（阻断）、sanitize（脱敏替换）

## 代码示例

运行基础示例：

```bash
python example.py
```

关键代码解读：

1. **InputGuard** — 维护拦截关键词列表，查询包含不当内容时直接拒绝，不进入 LLM
2. **OutputGuard** — 检查响应格式（如必须以"结论:"开头），不符合则拦截
3. **BusinessGuard** — 强制业务规则，如禁止响应中出现"内部定价""成本价"
4. **GuardrailsSystem** — 请求依次通过三层护栏，任一拦截则阻断并返回拒绝理由

合法请求通过所有护栏，非法请求在第一层就被拦截：这就是 Guardrails 的安全边界作用。

## 进阶示例

运行进阶示例：

```bash
python advanced.py
```

进阶示例展示三种护栏类型及其差异化失败处理：

1. **ContentSafetyGuard** — 拦截有害内容（武器、危险药物），策略为 block（直接阻断）
2. **PIIGuard** — 检测手机号、身份证号、邮箱等隐私信息，策略为 sanitize（脱敏替换而非阻断）
3. **FormatGuard** — 确保 JSON 输出包含必填字段（answer、confidence），缺少则 block
4. **拦截日志** — 所有拦截记录在 log 中，可审计每次护栏触发的原因和策略

不同护栏类型使用不同策略：有害内容必须阻断，隐私信息只需脱敏，格式不符则阻断并提示缺失字段。

## 优缺点

**优点**
- 防止有害输出——输入和输出双重拦截，LLM 不会泄露危险信息
- 保护隐私数据——PII 脱敏策略确保用户隐私不被暴露
- 强制业务合规——业务规则护栏确保 LLM 遵守公司政策
- 可审计每次拦截——日志记录所有拦截原因，便于回溯和改进

**缺点**
- 过严的 guardrails 可能限制有用输出——误拦截正常请求
- 维护成本高——规则需要持续更新以应对新场景
- 多层 guardrails 增加延迟——每个护栏都是一次额外检查
- 规则冲突——不同护栏的规则可能相互矛盾

## 真实项目中的应用

- **NVIDIA NeMo Guardrails** — 开源护栏框架，支持对话流控制、内容安全、话题约束
- **Guardrails AI** — Python 库，为 LLM 输出提供结构化验证（类型、格式、范围检查）
- **OpenAI Moderation API** — 内容安全 API，检测仇恨、暴力、自伤等有害内容
- **各大 AI 产品的内容安全层** — ChatGPT、Claude 等产品内置多层护栏系统

## 进一步阅读

- [NVIDIA NeMo Guardrails 文档](https://docs.nvidia.com/neemo-guardrails/) — 开源护栏框架的完整使用指南
- [Guardrails AI 文档](https://www.guardrailsai.com/docs) — 结构化输出验证库
- Bai et al. — *Constitutional AI: Harmlessness from AI Feedback* (2022，Anthropic，用 AI 自我约束替代人工标注，探索护栏的新范式)
