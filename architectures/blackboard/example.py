"""黑板架构 (Blackboard Architecture) 最小化示例

多个专家模块通过共享黑板空间协作：各专家读写黑板，
对新信息做出反应。专家之间不直接通信——只通过黑板间接交互。
"""


# --- 黑板：共享数据空间，所有专家读写这里 ---
class Blackboard:
    def __init__(self):
        self._data = {}    # 当前黑板数据
        self._history = [] # 数据变更历史

    def write(self, key, value, expert_name):
        """专家写入新信息到黑板"""
        self._data[key] = value
        self._history.append((expert_name, key, value))
        print(f"  [{expert_name}] 写入黑板: {key}={value}")

    def read(self, key):
        """专家从黑板读取信息"""
        return self._data.get(key)

    def read_all(self):
        """读取黑板全部数据"""
        return dict(self._data)

    def show_history(self):
        print("[Blackboard] 变更历史:")
        for expert, key, value in self._history:
            print(f"  {expert} → {key}: {value}")


# --- 专家：各自独立，只读写黑板，不直接与其他专家通信 ---
class DataExpert:
    """专家1：负责收集原始数据"""
    def contribute(self, blackboard):
        blackboard.write("raw_data", [10, 25, 30, 15], "DataExpert")

class AnalysisExpert:
    """专家2：分析数据，写入分析结果"""
    def contribute(self, blackboard):
        data = blackboard.read("raw_data")
        if data is None:
            return
        avg = sum(data) / len(data)
        blackboard.write("avg", avg, "AnalysisExpert")
        blackboard.write("max", max(data), "AnalysisExpert")

class ReportExpert:
    """专家3：根据分析结果生成报告"""
    def contribute(self, blackboard):
        avg = blackboard.read("avg")
        max_val = blackboard.read("max")
        if avg is None:
            return
        report = f"均值={avg:.1f}, 最大值={max_val}"
        blackboard.write("report", report, "ReportExpert")


# --- 控制器：决定调用哪些专家（黑板架构的调度核心） ---
class Controller:
    def __init__(self, experts):
        self._experts = experts

    def run(self, blackboard):
        """依次激活各专家，直到黑板没有新变化"""
        print("[Controller] 开始黑板协作流程")
        for expert in self._experts:
            expert.contribute(blackboard)
        print("[Controller] 协作完成")


# --- 运行演示 ---
if __name__ == "__main__":
    bb = Blackboard()
    experts = [DataExpert(), AnalysisExpert(), ReportExpert()]
    controller = Controller(experts)

    print("=" * 45)
    print("Blackboard 演示: 专家通过黑板间接协作")
    print("=" * 45 + "\n")

    controller.run(bb)
    print()
    print(f"黑板最终数据: {bb.read_all()}")
    bb.show_history()
