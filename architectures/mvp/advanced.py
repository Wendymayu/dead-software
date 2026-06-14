"""MVP 进阶示例：模拟 Android MVP 架构

展示 Android MVP 的核心原则：
- View 接口: Activity 只实现 ViewContract，完全被动
- Presenter: 持有 View 接口引用（非具体 Activity），协调 Model 和 View
- Model: 数据层，独立于 Presenter 和 View
- 流程: 用户点击 → View 转发 → Presenter → Model → Presenter → View.update()
"""

from abc import ABC, abstractmethod


class UserViewContract(ABC):
    """Android MVP 的 View 接口: 定义 Activity 能做什么"""
    @abstractmethod
    def show_loading(self): pass
    @abstractmethod
    def show_users(self, users): pass
    @abstractmethod
    def show_error(self, msg): pass


class UserModel:
    """模拟 Android Repository: 数据源"""
    _users = [{"name": "Alice", "role": "admin"},
              {"name": "Bob", "role": "user"}]

    def fetch_users(self):
        print("  [Model] Repository.fetchUsers() → 2 条")
        return self._users


class UserPresenter:
    """Android MVP 的 Presenter: 逻辑中心，只依赖 View 接口"""
    def __init__(self, model, view: UserViewContract):
        self.model = model
        self.view = view  # 只依赖抽象接口，不依赖具体 Activity

    def on_load_users_clicked(self):
        """用户点击按钮 → View 转发到 Presenter → Presenter 协调"""
        print("[Presenter] on_load_users_clicked()")
        self.view.show_loading()
        users = self.model.fetch_users()
        if users:
            self.view.show_users(users)
        else:
            self.view.show_error("无数据")


class MainActivity(UserViewContract):
    """Android Activity: 完全被动，不含逻辑，只按 Presenter 指令更新"""
    def show_loading(self):
        print("  [Activity] 显示 ProgressBar...")

    def show_users(self, users):
        print("  [Activity] 更新 RecyclerView:")
        for u in users:
            print(f"    → {u['name']} ({u['role']})")

    def show_error(self, msg):
        print(f"  [Activity] Toast: {msg}")

    def on_button_click(self, presenter):
        """用户点击 → 立即转发给 Presenter，自己不做任何处理"""
        print("[View] 用户点击按钮 → 转发给 Presenter")
        presenter.on_load_users_clicked()


class DarkActivity(UserViewContract):
    """另一个 View 实现: Presenter 代码完全不变"""
    def show_loading(self):
        print("  [DarkActivity] 深色加载动画...")
    def show_users(self, users):
        print("  [DarkActivity] 深色列表:")
        for u in users:
            print(f"    > {u['name']} | {u['role']}")
    def show_error(self, msg):
        print(f"  [DarkActivity] 深色错误: {msg}")
    def on_button_click(self, presenter):
        print("[View] 用户点击 → 转发给 Presenter")
        presenter.on_load_users_clicked()


if __name__ == "__main__":
    model = UserModel()
    print("=" * 50)
    print("Android MVP 架构模拟")
    print("=" * 50 + "\n")

    print("--- MainActivity ---")
    activity = MainActivity()
    presenter = UserPresenter(model, activity)
    activity.on_button_click(presenter)

    print("\n--- DarkActivity (Presenter 代码不变) ---")
    dark = DarkActivity()
    presenter2 = UserPresenter(model, dark)
    dark.on_button_click(presenter2)
