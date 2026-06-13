"""MVP 进阶示例：View 接口抽象 + 多 View 切换

展示 MVP 的核心优势：
- View 只是一个被动接口，Presenter 通过接口驱动展示
- 切换 View（Console/GUI/Web）不影响 Presenter 和 Model
- Presenter 是唯一的逻辑中心，便于单元测试
"""


from abc import ABC, abstractmethod


# --- View 接口：Presenter 只依赖抽象 ---
class UserViewInterface(ABC):
    @abstractmethod
    def show_user(self, name, age):
        pass

    @abstractmethod
    def show_error(self, msg):
        pass

    @abstractmethod
    def show_success(self, msg):
        pass


class ConsoleView(UserViewInterface):
    def show_user(self, name, age):
        print(f"  [Console] 姓名: {name}, 年龄: {age}")

    def show_error(self, msg):
        print(f"  [Console] [X] {msg}")

    def show_success(self, msg):
        print(f"  [Console] [OK] {msg}")


class TableView(UserViewInterface):
    def show_user(self, name, age):
        print(f"  [Table] | {name:^10} | {age:^5} |")

    def show_error(self, msg):
        print(f"  [Table] | ERROR: {msg:^15} |")

    def show_success(self, msg):
        print(f"  [Table] | {msg:^15} |")


# --- Model ---
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


# --- Presenter：只依赖 ViewInterface，可搭配任何 View 实现 ---
class UserPresenter:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def update_user(self, name, age):
        print(f"[Presenter] 处理输入: name={name}, age={age}")
        if age < 0 or age > 150:
            self.view.show_error("年龄不合法")
            return
        self.model.set_data(name, age)
        self.view.show_success("用户更新完成")
        self.view.show_user(self.model.get_name(), self.model.get_age())


# --- 运行演示 ---
if __name__ == "__main__":
    model = UserModel()

    print("=" * 50)
    print("进阶演示: 切换 View 实现，Presenter 代码不变")
    print("=" * 50 + "\n")

    print("--- 使用 ConsoleView ---")
    presenter1 = UserPresenter(model, ConsoleView())
    presenter1.update_user("Alice", 30)
    presenter1.update_user("BadAge", -1)

    print("\n--- 切换为 TableView（Presenter 代码不变）---")
    presenter2 = UserPresenter(model, TableView())
    presenter2.update_user("Bob", 25)
