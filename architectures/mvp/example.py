"""MVP (Model-View-Presenter) 最小化示例

演示三角分离：Model(数据) / View(被动展示) / Presenter(全部逻辑)
Presenter 完全控制 View，View 不观察 Model——与 MVC 的关键区别。
"""


# --- Model：只持有数据，不通知任何人 ---
class UserModel:
    def __init__(self):
        self._name = ""
        self._age = 0

    def set_data(self, name, age):
        self._name = name
        self._age = age

    def get_name(self):
        return self._name

    def get_age(self):
        return self._age


# --- View：完全被动，只提供展示接口，由 Presenter 驱动 ---
class UserView:
    def show_user(self, name, age):
        print(f"  [View] 姓名: {name}, 年龄: {age}")

    def show_error(self, msg):
        print(f"  [View] 错误: {msg}")

    def show_success(self, msg):
        print(f"  [View] 成功: {msg}")


# --- Presenter：全部逻辑在这里，协调 Model 和 View ---
class UserPresenter:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def update_user(self, name, age):
        print(f"[Presenter] 收到输入: name={name}, age={age}")
        # Presenter 负责验证逻辑
        if age < 0 or age > 150:
            self.view.show_error("年龄不合法")
            return
        # Presenter 更新 Model，然后从 Model 取数据驱动 View
        self.model.set_data(name, age)
        self.view.show_success("用户更新完成")
        self.view.show_user(self.model.get_name(), self.model.get_age())


# --- 运行演示 ---
if __name__ == "__main__":
    model = UserModel()
    view = UserView()
    presenter = UserPresenter(model, view)

    print("=" * 40)
    print("MVP 演示: View 不观察 Model，Presenter 全权控制")
    print("=" * 40 + "\n")

    presenter.update_user("Alice", 30)
    print()
    presenter.update_user("Bob", -5)  # Presenter 验证失败，View 显示错误
