"""MVVM 进阶示例：模拟 Vue.js 响应式数据绑定

展示 Vue.js MVVM 的核心机制：
- Reactive: __setattr__ 拦截属性变化，自动触发依赖更新
- 双向绑定: View input → ViewModel → Model，ViewModel → View 更新
- 依赖追踪: 属性变化时通知所有注册的 watcher
- 流程: input 变化 → ViewModel 属性更新 → Model 同步 → View 自动刷新
"""


class ReactiveViewModel:
    """模拟 Vue 3 Proxy-based 响应式: 属性变化自动触发 watcher"""

    def __init__(self):
        self._watchers = {}   # key → [callback, ...]
        self._data = {"user_name": "Alice", "age": 30}
        self._model = BackendModel()

    def __getattr__(self, key):
        if key.startswith("_"):
            return super().__getattribute__(key)
        return self._data.get(key)

    def __setattr__(self, key, value):
        if key.startswith("_"):
            super().__setattr__(key, value)
            return
        old = self._data.get(key)
        self._data[key] = value
        print(f"  [reactive] {key}: '{old}' → '{value}'")
        # 触发所有依赖 watcher
        for cb in self._watchers.get(key, []):
            cb(value)

    def watch(self, key, callback):
        """模拟 Vue watch: 注册依赖回调"""
        self._watchers.setdefault(key, []).append(callback)

    def sync_to_model(self):
        """ViewModel → Model: 数据同步到后端"""
        self._model.save(self._data["user_name"], self._data["age"])
        print("  [ViewModel→Model] 数据同步到后端")


class BackendModel:
    """模拟后端 API: Vue 的 Model 层"""

    def save(self, name, age):
        print(f"  [Model] POST /api/users {{name: '{name}', age: {age}}}")


class View:
    """模拟 Vue 挂载的 DOM: 自动更新 + 双向绑定"""

    def __init__(self, vm: ReactiveViewModel):
        self.vm = vm
        # 注册 watcher: ViewModel 属性变化 → View 自动刷新
        vm.watch("user_name", lambda v: self._update("#name", v))
        vm.watch("age", lambda v: self._update("#age", str(v)))

    def _update(self, selector, value):
        print(f"  [View] 更新 {selector} → \"{value}\"")

    def render(self):
        print(f"  [View] 渲染: <span>{self.vm.user_name}</span> <span>{self.vm.age}岁</span>")

    def on_input(self, new_name):
        """双向绑定: 用户输入 → ViewModel → Model → View 自动刷新"""
        print(f"[View] input 事件: 用户输入 '{new_name}'")
        self.vm.user_name = new_name       # View → ViewModel
        self.vm.sync_to_model()            # ViewModel → Model


if __name__ == "__main__":
    vm = ReactiveViewModel()
    view = View(vm)

    print("=" * 50)
    print("Vue.js MVVM 响应式数据绑定模拟")
    print("=" * 50 + "\n")

    print("--- 1. 初始渲染 ---")
    view.render()

    print("\n--- 2. 响应式更新: ViewModel 属性变化 → View 自动刷新 ---")
    vm.age = 25

    print("\n--- 3. 双向绑定: View input → ViewModel → Model ---")
    view.on_input("Bob")

    print("\n--- 4. 再次修改 → 链路复现 ---")
    view.on_input("Charlie")
