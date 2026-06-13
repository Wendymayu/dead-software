"""模板方法模式 (Template Method Pattern) 最小化示例

演示父类定义算法骨架，子类填充具体步骤：
- mine() 是模板方法，固定了步骤顺序
- read_data / process / analyze 是可变步骤
- 子类只需实现差异部分，骨架复用
"""


from abc import ABC, abstractmethod


class DataMiner(ABC):
    """抽象类：定义数据挖掘的算法骨架"""

    def mine(self):
        """模板方法：固定步骤顺序"""
        print(f"[DataMiner] 开始数据挖掘 ({self.__class__.__name__})")
        data = self.read_data()
        processed = self.process(data)
        result = self.analyze(processed)
        print(f"[DataMiner] 完成 → {result}\n")

    @abstractmethod
    def read_data(self): ...

    @abstractmethod
    def process(self, data): ...

    @abstractmethod
    def analyze(self, processed): ...


class CSVMiner(DataMiner):
    """子类：每步填充 CSV 的具体实现"""

    def read_data(self):
        print("  [CSV] 从 CSV 文件读取数据")
        return "raw_csv_data"

    def process(self, data):
        print("  [CSV] 拆分逗号，去除空行")
        return "cleaned_csv"

    def analyze(self, processed):
        print("  [CSV] 统计列频次")
        return "csv_report"


class JSONMiner(DataMiner):
    """子类：每步填充 JSON 的具体实现"""

    def read_data(self):
        print("  [JSON] 从 JSON 文件读取数据")
        return "raw_json_data"

    def process(self, data):
        print("  [JSON] 解析键值对，去除 null")
        return "cleaned_json"

    def analyze(self, processed):
        print("  [JSON] 提取嵌套字段")
        return "json_report"


# --- 运行演示 ---
if __name__ == "__main__":
    print("=" * 40)
    print("模板方法模式演示：骨架复用，步骤定制")
    print("=" * 40 + "\n")

    CSVMiner().mine()
    JSONMiner().mine()
