"""插件架构 (Plugin Architecture) 最小化示例

演示核心系统 + 动态注册插件：核心提供注册表，插件实现标准接口。
添加新插件无需修改核心代码——只需注册即可。
"""


# --- 插件接口：所有插件必须实现 ---
class PluginInterface:
    """标准接口，插件必须提供 name 和 execute"""
    def name(self):
        raise NotImplementedError

    def execute(self, data):
        raise NotImplementedError


# --- 插件注册表：核心系统的一部分 ---
class PluginRegistry:
    def __init__(self):
        self._plugins = {}

    def register(self, plugin):
        """核心代码不需要知道插件具体是什么，只调用标准接口"""
        n = plugin.name()
        self._plugins[n] = plugin
        print(f"[Registry] 注册插件: {n}")

    def execute(self, plugin_name, data):
        plugin = self._plugins.get(plugin_name)
        if not plugin:
            print(f"[Registry] 插件 {plugin_name} 未找到")
            return None
        print(f"[Registry] 调用插件: {plugin_name}")
        return plugin.execute(data)

    def list_plugins(self):
        return list(self._plugins.keys())


# --- 具体插件：各自独立实现标准接口 ---
class EncryptPlugin(PluginInterface):
    def name(self):
        return "encrypt"

    def execute(self, data):
        print(f"  [EncryptPlugin] 加密: {data}")
        return f"ENC({data})"


class CompressPlugin(PluginInterface):
    def name(self):
        return "compress"

    def execute(self, data):
        print(f"  [CompressPlugin] 压缩: {data}")
        return f"ZIP({data})"


# --- 运行演示 ---
if __name__ == "__main__":
    registry = PluginRegistry()
    registry.register(EncryptPlugin())
    registry.register(CompressPlugin())

    print("=" * 40)
    print("Plugin 演示: 核心不修改，插件动态注册")
    print("=" * 40 + "\n")

    result = registry.execute("encrypt", "hello")
    print(f"  → 结果: {result}\n")

    result = registry.execute("compress", "big data")
    print(f"  → 结果: {result}\n")

    # 添加新插件只需 register，核心代码零修改
    class LogPlugin(PluginInterface):
        def name(self): return "log"
        def execute(self, data): print(f"  [LogPlugin] 记录: {data}"); return data

    registry.register(LogPlugin())
    registry.execute("log", "system event")
