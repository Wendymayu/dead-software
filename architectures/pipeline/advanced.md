# 管道架构进阶：OpenTelemetry Collector

## 软件简介

OpenTelemetry Collector 是 OpenTelemetry 项目提供的可观测性数据收集与处理引擎。它从各种来源接收指标、日志和链路数据，经过处理后导出到不同的后端系统。Collector 的设计目标是：与数据源解耦、与后端解耦、可配置、可扩展。

## 该软件的架构

OTEL Collector 采用管道(Pipeline)架构，数据流经三个核心阶段：

1. **Receiver（接收器）**：数据入口，支持多种协议
   - OTLP Receiver：接收 OpenTelemetry 原生协议数据
   - Prometheus Receiver：拉取 Prometheus 指标
   - Zipkin Receiver：接收 Zipkin 链路数据

2. **Processor（处理器）**：中间处理，可链式组合多个处理器
   - Batch Processor：将数据批量打包，减少网络请求
   - Attributes Processor：添加、修改或删除属性标签
   - Filter Processor：根据条件过滤掉不需要的数据
   - Transform Processor：对数据做格式转换

3. **Exporter（导出器）**：数据出口，发送到后端
   - OTLP Exporter：导出到 OTLP 后端
   - Prometheus Exporter：暴露为 Prometheus 指标端点
   - Console Exporter：输出到控制台（调试用）

关键设计原则：
- 管道可配置：通过 YAML 配置文件定义 Receiver→Processor→Exporter 的组合
- 多管道并行：可同时运行指标管道、日志管道、链路管道
- 每种管道只能有指定类型的数据流（metrics/logs/traces）

## 简化实现思路

我们的简化代码模拟了 OTEL Collector 最核心的管道机制：

- `MetricReceiver` → 对应 Receiver，解析原始指标字符串为结构化数据
- `Processor` → 对应 Processor，添加属性标签并过滤低值指标
- `ConsoleExporter` → 对应 Exporter，将处理后的数据输出到控制台
- `Pipeline` → 串联三个阶段，数据依次流过 Receiver→Processor→Exporter

代码中的数据流：`"cpu.usage=78.5"` → Receiver解析 → Processor添加属性+过滤 → Exporter输出

## 与真实实现的对照

| 简化代码 | 真实 OTEL Collector | 说明 |
|---------|-------------------|------|
| `MetricReceiver` | OTLP/Prometheus Receiver | 真实Receiver支持多种协议解析，我们只做简单字符串解析 |
| `Processor(min_value, extra_attrs)` | Batch/Attributes/Filter Processor | 真实有多个Processor可链式组合，我们合并为一个 |
| `ConsoleExporter` | OTLP/Prometheus/Console Exporter | 真实Exporter支持多种后端协议，我们只输出到控制台 |
| `Pipeline.run()` | YAML配置驱动的管道 | 真实通过配置文件组合管道，我们硬编码阶段顺序 |
| 单一管道 | 多管道(metrics/logs/traces) | 真实支持三类管道并行运行 |

## 学习建议

1. **理解管道本质**：管道就是"数据流经一系列处理阶段"，每个阶段只做一件事
2. **关注可配置性**：OTEL Collector 的强大在于配置驱动，不修改代码就能改变数据流
3. **动手实验**：下载 OTEL Collector，写一个简单 YAML 配置，观察数据从 Receiver 到 Exporter 的流转
4. **对比思考**：管道架构 vs 事件驱动架构 — 管道是顺序的，事件驱动是异步的
5. **扩展阅读**：OTEL Collector 的 Extensions 机制（健康检查、pprof等）展示了管道之外的辅助组件设计
