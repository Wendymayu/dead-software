# Dead-Software

> 软件工程架构与设计模式的阅读资料，配有简单但可运行的代码示例。

## 为什么有这个项目

AI coding 正在深刻改变软件工程——代码生成、调试、重构，AI 都能做，而且做得越来越快。

但这带来一个隐患：**新入门的工程师可能跳过了传统的成长经历**。过去，你在反复手写和踩坑中自然建立起对架构和设计的判断力——什么时候该用微服务，什么时候分层就够了；哪段代码藏着紧耦合，哪种抽象其实是过度设计。这些判断力不是来自"会写代码"，而是来自"写过很多代码后知道什么代码不该写"。

AI 让你不再需要"手熟"，但反而更需要"眼毒"。

- 手写代码的能力贬值了——AI 比你快、比你不犯错
- 判断代码的能力升值了——AI 给你方案，但你得判断这个方案在你的场景下是否合理
- 架构选择的权力还在你手里——AI 不知道你的团队大小、业务阶段、组织约束

**判断力的来源，就是对架构和设计模式的轮廓理解**——不是每个实现细节，而是每个模式的：为什么存在、什么场景适用、有什么代价。

这正是这个项目要做的事：**不是教你写代码，而是帮你建立判断力。**

项目名 "dead-software" 不是一个悲观的名字。它是一个提醒——传统的"手写软件"方式正在消亡，但软件工程的思想不会。理解这些思想，你才能在 AI coding 时代做一个有判断力的工程师，而不是一个只会点确认按钮的操作员。

## 项目简介

本项目覆盖软件工程的核心知识体系，每个主题配有简洁讲解和最小化可运行代码：

- **架构模式** — 系统的宏观结构：分层、事件驱动、微服务、CQRS、六边形、单体、MVVM、Actor、事件溯源、Saga……
- **设计模式** — 代码的微观结构：观察者、策略、工厂、装饰器、命令、适配器、代理、状态……
- **SOLID 原则** — 设计模式背后的理论根基
- **并发模式** — 异步与并发的基本范式
- **反模式** — 知道什么是错的，比知道什么是对的更能防止犯错
- **AI & Agent 架构** — RAG、ReAct、Tool Use、Multi-Agent、MCP、Memory、Guardrails……当前最活跃的架构领域

每个主题不需要你手写实现，而是让你读完之后能回答三个问题：**它解决什么问题？什么时候该用？用了要付出什么代价？**

完整主题规划见 [docs/roadmap.md](docs/roadmap.md)。

## 如何使用

每个主题目录包含：
- `README.md` — 概念讲解、优缺点、真实项目应用、延伸阅读
- `example.py` — 最小化可运行示例（`python example.py` 即可运行）
- `advanced.py` — 进阶示例（部分主题提供）

不需要安装任何依赖：

```bash
python architectures/layered/example.py
python design-patterns/observer/example.py
```

## 已完成主题

### 架构模式

| 主题 | 目录 | 核心演示 |
|------|------|----------|
| 分层架构 | [architectures/layered/](architectures/layered/) | 三层分离（展示层/业务层/数据层） |
| 事件驱动架构 | [architectures/event-driven/](architectures/event-driven/) | 事件总线 + 发布订阅 |
| 微服务架构 | [architectures/microservices/](architectures/microservices/) | 独立服务通过 HTTP 通信 |
| 管道架构 | [architectures/pipeline/](architectures/pipeline/) | 数据经过多个处理阶段流转 |
| 单体架构 | [architectures/monolithic/](architectures/monolithic/) | 所有功能在一个应用中 |
| MVC | [architectures/mvc/](architectures/mvc/) | Model-View-Controller 三角分离 |
| MVVM | [architectures/mvvm/](architectures/mvvm/) | 数据绑定驱动视图 |
| 六边形架构 | [architectures/hexagonal/](architectures/hexagonal/) | 端口与适配器，核心不依赖外部 |
| CQRS | [architectures/cqrs/](architectures/cqrs/) | 命令与查询分离，读写模型独立 |
| 无服务器架构 | [architectures/serverless/](architectures/serverless/) | 函数即服务，按调用计费 |
| 事件溯源 | [architectures/event-sourcing/](architectures/event-sourcing/) | 以事件序列替代传统状态存储 |
| 绞杀者模式 | [architectures/strangler/](architectures/strangler/) | 逐步用新系统替换旧系统 |
| Saga | [architectures/saga/](architectures/saga/) | 微服务下的分布式长事务协调 |
| REST 架构 | [architectures/rest/](architectures/rest/) | 资源 + 统一接口 + 无状态通信 |

### 设计模式

| 主题 | 目录 | 核心演示 |
|------|------|----------|
| 观察者模式 | [design-patterns/observer/](design-patterns/observer/) | 一对多依赖通知 |
| 策略模式 | [design-patterns/strategy/](design-patterns/strategy/) | 算法族可互换封装 |
| 工厂模式 | [design-patterns/factory/](design-patterns/factory/) | 对象创建逻辑集中管理 |
| 装饰器模式 | [design-patterns/decorator/](design-patterns/decorator/) | 动态给对象添加职责 |

## 代码原则

- 纯 Python 标准库，无需安装额外依赖
- 单文件可运行：`python example.py` 即可看到输出
- 最小化示例：只演示核心机制，通常 < 80 行
- 输出驱动：运行结果清晰展示架构/模式的作用
- 注释解释 why，不只是 what——连接代码与概念

## 贡献

欢迎添加新的架构模式或设计模式主题。每个新主题请遵循已有目录的 README.md 模板和代码原则。完整规划见 [docs/roadmap.md](docs/roadmap.md)。
