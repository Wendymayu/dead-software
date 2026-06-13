# Dead-Software

> 软件工程架构与设计模式的阅读资料，配有简单但可运行的代码示例。

AI coding 正在深刻改变软件工程。新入门的工程师可能缺少传统的成长经历，但对软件工程的整体了解仍然不可或缺。本项目提供常见架构模式和设计模式的讲解与最小化可运行示例，帮助你快速建立软件工程的宏观认知。

## 如何使用

每个主题目录包含：
- `README.md` — 概念讲解、优缺点、真实项目应用、延伸阅读
- `example.py` — 最小化可运行示例（`python example.py` 即可运行）
- `advanced.py` — 进阶示例（部分主题提供）

## 架构模式 (Architecture Patterns)

| 主题 | 目录 | 核心演示 |
|------|------|----------|
| 分层架构 | [architectures/layered/](architectures/layered/) | 三层分离（展示层/业务层/数据层） |
| 事件驱动架构 | [architectures/event-driven/](architectures/event-driven/) | 事件总线 + 发布订阅 |
| 微服务架构 | [architectures/microservices/](architectures/microservices/) | 独立服务通过 HTTP 通信 |
| 管道架构 | [architectures/pipeline/](architectures/pipeline/) | 数据经过多个处理阶段流转 |

## 设计模式 (Design Patterns)

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

## 贡献

欢迎添加新的架构模式或设计模式主题。每个新主题请遵循已有目录的 README.md 模板和代码原则。
