"""插件架构进阶示例：自动发现 + 插件生命周期

展示插件架构的进阶能力：
- 自动发现：扫描已注册插件，无需手动配置
- 生命周期：初始化 → 执行 → 清理
- 插件优先级和链式执行
"""


# --- 插件接口：增加生命周期方法 ---
class PluginInterface:
    def name(self):
        raise NotImplementedError

    def priority(self):
        return 0  # 默认优先级，数值越小越先执行

    def initialize(self):
        print(f"  [{self.name()}] 初始化完成")

    def execute(self, data):
        raise NotImplementedError

    def teardown(self):
        print(f"  [{self.name()}] 清理完成")


# --- 注册表：自动发现 + 生命周期管理 + 链式执行 ---
class PluginRegistry:
    def __init__(self):
        self._plugins = []

    def discover_and_register(self, plugins):
        """自动发现并注册一批插件"""
        print("[Registry] 自动发现插件...")
        for p in plugins:
            self._plugins.append(p)
            print(f"  发现: {p.name()} (优先级: {p.priority()})")
        # 按优先级排序
        self._plugins.sort(key=lambda p: p.priority())

    def initialize_all(self):
        print("[Registry] 初始化所有插件...")
        for p in self._plugins:
            p.initialize()

    def execute_chain(self, data):
        """链式执行：数据依次通过所有插件"""
        print(f"[Registry] 链式处理: {data}")
        result = data
        for p in self._plugins:
            print(f"  → 经过 {p.name()}")
            result = p.execute(result)
        return result

    def teardown_all(self):
        print("[Registry] 清理所有插件...")
        for p in self._plugins:
            p.teardown()


# --- 具体插件 ---
class ValidatePlugin(PluginInterface):
    def name(self): return "validate"
    def priority(self): return 1  # 最先执行
    def execute(self, data):
        print(f"    [Validate] 检查: '{data}' 非空")
        return data.strip()


class TransformPlugin(PluginInterface):
    def name(self): return "transform"
    def priority(self): return 2
    def execute(self, data):
        print(f"    [Transform] 转大写: '{data}'")
        return data.upper()


class OutputPlugin(PluginInterface):
    def name(self): return "output"
    def priority(self): return 3  # 最后执行
    def execute(self, data):
        print(f"    [Output] 输出: '{data}'")
        return f"RESULT: {data}"


# --- 运行演示 ---
if __name__ == "__main__":
    registry = PluginRegistry()

    print("=" * 50)
    print("进阶演示: 自动发现 + 生命周期 + 链式执行")
    print("=" * 50 + "\n")

    registry.discover_and_register([ValidatePlugin(), TransformPlugin(), OutputPlugin()])
    registry.initialize_all()
    print()
    result = registry.execute_chain("  hello world  ")
    print(f"\n最终结果: {result}")
    registry.teardown_all()
