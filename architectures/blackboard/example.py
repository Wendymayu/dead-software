"""黑板架构 (Blackboard Architecture) 最小化示例

多个专家模块通过共享黑板空间协作：各专家读写黑板，
对新信息做出反应。专家之间不直接通信——只通过黑板间接交互。
"""


# --- 黑板：共享数据空间，所有专家读写这里 ---
class Blackboard:
    def __init__(self):
        self._data = {}
        self._history = []

    def write(self, key, value, expert_name):
        self._data[key] = value
        self._history.append((expert_name, key, value))
        print(f"  [{expert_name}] 写入黑板: {key}={value}")

    def read(self, key):
        return self._data.get(key)

    def read_all(self):
        return dict(self._data)

    def show_history(self):
        print("[Blackboard] 变更历史:")
        for expert, key, value in self._history:
            print(f"  {expert} -> {key}: {value}")


# --- 专家：各自独立，只读写黑板，不直接与其他专家通信 ---
class DataExpert:
    def contribute(self, bb):
        bb.write("raw_data", [10, 25, 30, 15], "DataExpert")

class AnalysisExpert:
    def contribute(self, bb):
        data = bb.read("raw_data")
        if data is None: return
        bb.write("avg", sum(data) / len(data), "AnalysisExpert")
        bb.write("max", max(data), "AnalysisExpert")

class ReportExpert:
    def contribute(self, bb):
        avg, max_val = bb.read("avg"), bb.read("max")
        if avg is None: return
        bb.write("report", f"均值={avg:.1f}, 最大值={max_val}", "ReportExpert")


# --- 控制器：决定调用哪些专家（黑板架构的调度核心） ---
class Controller:
    def __init__(self, experts):
        self._experts = experts

    def run(self, bb):
        print("[Controller] 开始黑板协作流程")
        for expert in self._experts:
            expert.contribute(bb)
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
    print(f"\n黑板最终数据: {bb.read_all()}")
    bb.show_history()
