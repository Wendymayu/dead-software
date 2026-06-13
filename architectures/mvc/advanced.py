"""MVC 进阶示例：Model 驱动多个独立 View

展示 MVC 的核心优势：
- 同一个 Model 变化时，所有 View 自动同步更新
- 新增 View 不需要修改 Model 或 Controller
- View 只关心如何展示，不知道数据从哪来
"""


class UserModel:
    """Model: 用户数据 + 业务规则"""

    def __init__(self):
        self._name = ""
        self._age = 0
        self._views = []

    def attach(self, view):
        self._views.append(view)

    def set_user(self, name, age):
        self._name = name
        self._age = age
        self._notify()

    def _notify(self):
        # Model 变化 → 推送给所有 View，View 各自决定如何展示
        for view in self._views:
            view.update(name=self._name, age=self._age)


class ProfileView:
    """View: 个人资料卡片展示"""

    def update(self, name, age):
        print(f"  [ProfileView] ========== {name} ({age}岁) ==========")


class ListView:
    """View: 列表展示"""

    def update(self, name, age):
        print(f"  [ListView] - {name}, 年龄 {age}")


class FormController:
    """Controller: 处理用户输入，更新 Model"""

    def __init__(self, model):
        self.model = model

    def submit_form(self, name, age):
        print(f"[Controller] 提交表单: name={name}, age={age}")
        self.model.set_user(name, age)


# --- 运行演示 ---
if __name__ == "__main__":
    model = UserModel()
    model.attach(ProfileView())
    model.attach(ListView())

    controller = FormController(model)

    print("=" * 50)
    print("进阶演示: 同一 Model → 多个 View 自动同步")
    print("=" * 50 + "\n")

    controller.submit_form("Alice", 30)
    print()
    controller.submit_form("Bob", 25)
