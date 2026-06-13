"""外观模式 (Facade Pattern) 最小化示例

演示简化复杂子系统的访问接口：
- 外观类提供一个统一的高层接口
- 客户端无需了解子系统内部的复杂交互
- 子系统本身不受影响，仍可独立使用
"""


class LightSystem:
    """子系统：灯光控制（内部有复杂API）"""

    def turn_on(self, brightness=100):
        print(f"    [灯光] 开灯，亮度={brightness}%")

    def turn_off(self):
        print("    [灯光] 关灯")


class ACSystem:
    """子系统：空调控制（内部有复杂API）"""

    def set_temperature(self, temp, mode="cool"):
        print(f"    [空调] 设置温度={temp}C，模式={mode}")


class TVSystem:
    """子系统：电视控制（内部有复杂API）"""

    def turn_on(self, channel=1):
        print(f"    [电视] 开机，频道={channel}")


class HomeAutomationFacade:
    """外观：一键控制多个子系统"""

    def __init__(self):
        self._light = LightSystem()
        self._ac = ACSystem()
        self._tv = TVSystem()

    def leave_home(self):
        """一键离家：关灯、关空调、关电视"""
        print("[外观] 执行「离家模式」")
        self._light.turn_off()
        self._ac.set_temperature(26, mode="off")
        self._tv.turn_on(channel=0)  # channel=0 = 关机

    def movie_mode(self):
        """一键观影：调暗灯光、调低空调、开电视"""
        print("[外观] 执行「观影模式」")
        self._light.turn_on(brightness=30)
        self._ac.set_temperature(24)
        self._tv.turn_on(channel=5)


# --- 运行演示 ---
if __name__ == "__main__":
    print("=" * 40)
    print("外观模式演示：一键控制智能家居子系统")
    print("=" * 40 + "\n")

    facade = HomeAutomationFacade()

    facade.movie_mode()
    print()

    facade.leave_home()
