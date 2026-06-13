"""MVVM (Model-View-ViewModel) 最小化示例

演示数据绑定驱动的展示架构：
- Model: 原始数据和业务逻辑
- ViewModel: 将 Model 数据转换为 View 可直接使用的格式
- View: 只关心展示，通过绑定 ViewModel 自动更新
"""


class UserModel:
    """Model: 原始数据 + 业务规则"""

    def __init__(self):
        self._name = "alice"
        self._age = 30

    def get_name(self):
        return self._name

    def get_age(self):
        return self._age

    def set_name(self, name):
        self._name = name

    def set_age(self, age):
        self._age = age


class UserViewModel:
    """ViewModel: 转换 Model 数据为 View 友好格式，管理展示状态"""

    def __init__(self, model):
        self.model = model
        self._views = []

    def attach(self, view):
        self._views.append(view)

    # --- 将原始数据转换为展示格式 ---
    def display_name(self):
        return self.model.get_name().capitalize()

    def display_age(self):
        return f"{self.model.get_age()}岁"

    def display_summary(self):
        return f"{self.display_name()} ({self.display_age()})"

    # --- 更新数据后自动通知 View ---
    def set_name(self, name):
        self.model.set_name(name)
        self._notify()

    def set_age(self, age):
        self.model.set_age(age)
        self._notify()

    def _notify(self):
        for view in self._views:
            view.update(self)


class UserView:
    """View: 只关心如何展示 ViewModel 提供的数据"""

    def update(self, vm):
        print(f"  [View] 姓名: {vm.display_name()}")
        print(f"  [View] 年龄: {vm.display_age()}")
        print(f"  [View] 概要: {vm.display_summary()}")


# --- 运行演示 ---
if __name__ == "__main__":
    model = UserModel()
    vm = UserViewModel(model)
    vm.attach(UserView())

    print("=" * 40)
    print("MVVM 演示: Model → ViewModel(转换) → View(绑定)")
    print("=" * 40 + "\n")

    # ViewModel 自动将 "alice" 转为 "Alice" 展示
    print("--- 初始状态 ---")
    print(f"  Model原始数据: name={model.get_name()}, age={model.get_age()}")
    print(f"  ViewModel转换后: {vm.display_summary()}\n")

    print("--- 修改数据，View 自动更新 ---")
    vm.set_name("bob")
    vm.set_age(25)
