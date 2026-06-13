"""MVVM 进阶示例：双向数据绑定

展示 MVVM 与 MVC 的关键区别：
- 不仅 Model → View (单向绑定)
- View 的输入也通过 ViewModel 回写到 Model (双向绑定)
- ViewModel 是唯一的中间人，View 和 Model 不直接通信
"""


class TemperatureModel:
    def __init__(self):
        self._celsius = 0

    def set_celsius(self, c):
        self._celsius = c

    def get_celsius(self):
        return self._celsius


class TemperatureViewModel:
    """ViewModel: 负责双向转换 C ↔ F，View 只看到 ViewModel"""

    def __init__(self, model):
        self.model = model
        self._views = []

    def attach(self, view):
        self._views.append(view)

    # --- Model → View 转换 ---
    def display_celsius(self):
        return f"{self.model.get_celsius()}C"

    def display_fahrenheit(self):
        f = self.model.get_celsius() * 9 / 5 + 32
        return f"{f:.1f}F"

    # --- View → Model 回写 ---
    def set_celsius(self, c):
        print(f"  [ViewModel] 输入摄氏: {c}C → 更新Model")
        self.model.set_celsius(c)
        self._notify()

    def set_fahrenheit(self, f):
        c = (f - 32) * 5 / 9
        print(f"  [ViewModel] 输入华氏: {f}F → 转换为 {c:.1f}C → 更新Model")
        self.model.set_celsius(c)
        self._notify()

    def _notify(self):
        for view in self._views:
            view.update(self)


class TemperatureView:
    """View: 同时展示 C 和 F，通过 ViewModel 双向交互"""

    def update(self, vm):
        print(f"    [View] {vm.display_celsius()} / {vm.display_fahrenheit()}")

    def input_celsius(self, vm, c):
        print(f"\n[View] 用户输入摄氏 {c}C")
        vm.set_celsius(c)

    def input_fahrenheit(self, vm, f):
        print(f"\n[View] 用户输入华氏 {f}F")
        vm.set_fahrenheit(f)


# --- 运行演示 ---
if __name__ == "__main__":
    model = TemperatureModel()
    vm = TemperatureViewModel(model)
    view = TemperatureView()
    vm.attach(view)

    print("=" * 50)
    print("进阶演示: 双向绑定 -- C <-> F 自动转换")
    print("=" * 50 + "\n")

    view.input_celsius(vm, 100)   # 输入100C → View显示100C/212F
    view.input_fahrenheit(vm, 68) # 输入68F → 转换为20C → View显示20C/68F
