"""管道架构进阶示例：模拟 OpenTelemetry Collector 管道

展示 OTEL Collector 的核心数据流：
Receiver → Processor → Exporter
指标数据依次经过接收、处理、导出三个阶段。
"""


# --- Receiver：接收原始指标数据 ---
class MetricReceiver:
    """模拟 OTEL Receiver，解析传入的指标字符串"""

    def receive(self, raw: str) -> dict:
        name, value = raw.split("=")
        metric = {"name": name, "value": float(value), "attributes": {}}
        print(f"[Receiver] 接收指标: {name}={value}")
        return metric


# --- Processor：添加属性 + 过滤 ---
class Processor:
    """模拟 OTEL Processor，为指标添加属性并过滤低值"""

    def __init__(self, min_value=0, extra_attrs=None):
        self.min_value = min_value
        self.extra_attrs = extra_attrs or {"env": "production", "region": "cn-east"}

    def process(self, metric: dict) -> dict | None:
        metric["attributes"] = self.extra_attrs
        print(f"[Processor] 添加属性: {metric['attributes']}")
        if metric["value"] < self.min_value:
            print(f"[Processor] 过滤低值指标: {metric['name']}={metric['value']}")
            return None
        print(f"[Processor] 保留指标: {metric['name']}={metric['value']}")
        return metric


# --- Exporter：输出到目标 ---
class ConsoleExporter:
    """模拟 OTEL Exporter，将处理后的指标输出到控制台"""

    def export(self, metric: dict) -> None:
        print(f"[Exporter] 导出 → name={metric['name']} "
              f"value={metric['value']} attrs={metric['attributes']}")


# --- Pipeline：串联三个阶段 ---
class Pipeline:
    """OTEL Collector 管道：Receiver → Processor → Exporter"""

    def __init__(self, receiver, processor, exporter):
        self.receiver = receiver
        self.processor = processor
        self.exporter = exporter

    def run(self, raw_metrics: list[str]):
        print("=" * 50)
        print("OTEL Collector 管道: Receiver → Processor → Exporter")
        print("=" * 50)
        for raw in raw_metrics:
            print(f"\n--- 处理: '{raw}' ---")
            metric = self.receiver.receive(raw)
            processed = self.processor.process(metric)
            if processed:
                self.exporter.export(processed)
            else:
                print("[Pipeline] 数据被过滤，未导出")


if __name__ == "__main__":
    pipeline = Pipeline(
        MetricReceiver(),
        Processor(min_value=5),
        ConsoleExporter(),
    )
    pipeline.run(["cpu.usage=78.5", "mem.free=2.1", "disk.io=45.0"])
