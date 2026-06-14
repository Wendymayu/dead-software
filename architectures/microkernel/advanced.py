"""微内核进阶示例：模拟 Eclipse RCP 微内核

展示 Eclipse RCP 的微内核架构：
- EclipseCore（极薄核心）：仅提供工作台窗口管理 + 扩展点注册表
- 所有功能（编辑器/视图/透视图）都是扩展，通过扩展点注册
- JavaEditorExtension 通过 org.eclipse.ui.editors 扩展点注册
"""

class ExtensionPoint:
    """扩展点：内核定义的契约插槽"""
    def __init__(self, id, desc):
        self._id, self._desc = id, desc
        self._contributions = []

    def contribute(self, plugin_id, element):
        self._contributions.append((plugin_id, element))
        print(f"  [{plugin_id}] 向 '{self._id}' 贡献: {element}")

    def list_all(self):
        print(f"[{self._id}] 扩展点 '{self._desc}' 的贡献:")
        for pid, elem in self._contributions: print(f"  - {pid}: {elem}")


class EclipseCore:
    """Eclipse RCP 微内核：极薄核心——仅窗口管理 + 扩展点"""
    def __init__(self):
        self._registry, self._windows = {}, []

    def define_extension_point(self, id, desc):
        """内核定义扩展点——微内核唯一提供的契约"""
        self._registry[id] = ExtensionPoint(id, desc)
        print(f"[EclipseCore] 定义扩展点: {id} ({desc})")

    def get_point(self, id): return self._registry[id]

    def install_plugin(self, plugin_id, contributions):
        """安装插件——向扩展点贡献功能"""
        print(f"[EclipseCore] 安装插件: {plugin_id}")
        for point_id, element in contributions:
            self.get_point(point_id).contribute(plugin_id, element)

    def open_window(self, title):
        """窗口管理——内核提供的唯一运行时功能"""
        self._windows.append(title)
        print(f"[EclipseCore] 打开工作台窗口: {title}")

    def render(self):
        """根据注册的贡献渲染完整 IDE"""
        print(f"\n[EclipseCore] 渲染 IDE (窗口: {self._windows}):")
        print("=" * 40)
        for point in self._registry.values(): point.list_all()
        print("=" * 40)


class JavaEditorExtension:
    """Java 编辑器扩展：通过 org.eclipse.ui.editors 扩展点注册"""
    PLUGIN_ID = "org.eclipse.jdt.ui"

    @staticmethod
    def install(core):
        core.install_plugin(JavaEditorExtension.PLUGIN_ID, [
            ("org.eclipse.ui.editors", "JavaEditor (编辑 .java 文件)"),
            ("org.eclipse.ui.views", "PackageExplorer (包浏览器)"),
            ("org.eclipse.ui.menus", "Edit→Format Code"),
        ])


if __name__ == "__main__":
    print("=" * 50)
    print("进阶演示: 模拟 Eclipse RCP 微内核架构")
    print("=" * 50 + "\n")

    core = EclipseCore()
    # 微内核定义扩展点——这是核心提供的唯一契约
    core.define_extension_point("org.eclipse.ui.editors", "编辑器插槽")
    core.define_extension_point("org.eclipse.ui.views", "视图插槽")
    core.define_extension_point("org.eclipse.ui.menus", "菜单插槽")
    core.define_extension_point("org.eclipse.ui.perspectives", "透视图插槽")

    # 所有 IDE 功能都是扩展——包括 Java 编辑器
    print("--- 安装扩展（核心不包含任何 IDE 功能）---")
    JavaEditorExtension.install(core)
    core.install_plugin("org.eclipse.debug", [("org.eclipse.ui.views", "DebugView"), ("org.eclipse.ui.menus", "Run→Debug")])
    core.install_plugin("org.eclipse.search", [("org.eclipse.ui.views", "SearchView"), ("org.eclipse.ui.menus", "Search→Find")])

    # 内核打开工作台窗口，扩展贡献填充内容
    core.open_window("Eclipse IDE")
    core.render()
