"""MVC (Model-View-Controller) 最小化示例

演示三角分离：Model(数据+逻辑) / View(展示) / Controller(输入+协调)
Controller 接收输入 → 更新 Model → Model 通知 View 更新展示
"""


class TemperatureModel:
    """Model: 持有数据，提供业务逻辑"""

    def __init__(self):
        self._temperature = 0
        self._views = []

    def attach(self, view):
        self._views.append(view)

    def set_temperature(self, temp):
        self._temperature = temp
        # Model 变化时主动通知所有绑定的 View（Observer 模式）
        for view in self._views:
            view.update(self._temperature)

    def get_temperature(self):
        return self._temperature


class TextView:
    """View: 只负责展示数据"""

    def update(self, temperature):
        print(f"  [TextView] 当前温度: {temperature}C")


class ChartView:
    """View: 另一种展示方式"""

    def update(self, temperature):
        bar = "|" * max(0, temperature)
        print(f"  [ChartView] 温度条: {bar} ({temperature}C)")


class TemperatureController:
    """Controller: 接收输入，协调 Model 和 View"""

    def __init__(self, model):
        self.model = model

    def set_temperature(self, temp):
        print(f"[Controller] 收到输入: 设置温度为 {temp}C")
        # Controller 不直接操作 View，而是通过 Model 间接触发更新
        self.model.set_temperature(temp)

    def increase(self):
        new_temp = self.model.get_temperature() + 1
        self.set_temperature(new_temp)


# --- 运行演示 ---
if __name__ == "__main__":
    model = TemperatureModel()
    model.attach(TextView())
    model.attach(ChartView())

    controller = TemperatureController(model)

    print("=" * 40)
    print("MVC 演示: Controller → Model → View")
    print("=" * 40 + "\n")

    controller.set_temperature(10)
    controller.set_temperature(25)
    controller.increase()  # Controller 操作 Model，Model 自动更新 View
