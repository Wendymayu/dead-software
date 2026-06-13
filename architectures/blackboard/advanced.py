"""黑板架构进阶示例：条件触发 + 多轮迭代

展示黑板架构的进阶能力：
- 条件触发：专家只在黑板满足特定条件时才参与
- 多轮迭代：控制器反复激活专家，直到黑板稳定
- 专家可触发新条件——形成级联效应
"""


class Blackboard:
    def __init__(self):
        self._data = {}
        self._changes = 0  # 本轮变更计数

    def write(self, key, value, expert_name):
        old = self._data.get(key)
        if old != value:
            self._data[key] = value
            self._changes += 1
            print(f"  [{expert_name}] 写入: {key}={value}")

    def read(self, key):
        return self._data.get(key)

    def read_all(self):
        return dict(self._data)

    def reset_changes(self):
        self._changes = 0

    def has_changes(self):
        return self._changes > 0


class Expert:
    """专家基类：带条件判断"""
    def can_contribute(self, bb):
        """判断黑板是否满足参与条件"""
        raise NotImplementedError

    def contribute(self, bb):
        raise NotImplementedError


class SensorExpert(Expert):
    """提供原始传感器数据"""
    def can_contribute(self, bb):
        return bb.read("sensor_data") is None  # 黑板还没有传感器数据

    def contribute(self, bb):
        bb.write("sensor_data", {"temp": 38, "humidity": 80}, "SensorExpert")


class DiagnosisExpert(Expert):
    """根据传感器数据诊断问题"""
    def can_contribute(self, bb):
        data = bb.read("sensor_data")
        return data is not None and bb.read("diagnosis") is None

    def contribute(self, bb):
        data = bb.read("sensor_data")
        if data["temp"] > 35 and data["humidity"] > 70:
            bb.write("diagnosis", "高温高湿-设备过热风险", "DiagnosisExpert")
            bb.write("risk_level", "HIGH", "DiagnosisExpert")
        else:
            bb.write("diagnosis", "环境正常", "DiagnosisExpert")
            bb.write("risk_level", "LOW", "DiagnosisExpert")


class AlertExpert(Expert):
    """根据风险等级发出告警"""
    def can_contribute(self, bb):
        return bb.read("risk_level") is not None and bb.read("alert") is None

    def contribute(self, bb):
        risk = bb.read("risk_level")
        if risk == "HIGH":
            bb.write("alert", "紧急告警: 立即降温除湿!", "AlertExpert")
        else:
            bb.write("alert", "正常: 无需处理", "AlertExpert")


class Controller:
    """多轮迭代调度——反复激活满足条件的专家"""
    def __init__(self, experts, max_rounds=5):
        self._experts = experts
        self._max_rounds = max_rounds

    def run(self, bb):
        print("[Controller] 开始多轮黑板协作")
        for round_num in range(1, self._max_rounds + 1):
            bb.reset_changes()
            print(f"\n--- 第 {round_num} 轮 ---")
            for expert in self._experts:
                if expert.can_contribute(bb):
                    expert.contribute(bb)
            if not bb.has_changes():
                print(f"\n[Controller] 第 {round_num} 轮无变更，黑板稳定")
                break


# --- 运行演示 ---
if __name__ == "__main__":
    bb = Blackboard()
    experts = [SensorExpert(), DiagnosisExpert(), AlertExpert()]
    controller = Controller(experts)

    print("=" * 50)
    print("进阶演示: 条件触发 + 多轮迭代直到黑板稳定")
    print("=" * 50 + "\n")

    controller.run(bb)
    print(f"\n黑板最终数据: {bb.read_all()}")
