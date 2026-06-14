"""插件架构进阶示例：模拟 VS Code 扩展系统

展示 VS Code 的核心插件架构：
- ExtensionRegistry：扩展注册能力（命令/语言/主题）
- 濒加载：扩展仅在激活事件触发时才初始化
- PythonLintExtension 注册命令和语言支持，打开 .py 文件时激活
"""

class Extension:
    """VS Code 扩展：声明能力与激活条件"""
    def __init__(self, name, capabilities, activation_on):
        self._name, self._capabilities, self._activation_on = name, capabilities, activation_on
        self._activated = False

    def activate(self):
        if self._activated: return
        self._activated = True
        print(f"[Extension:{self._name}] 濒加载激活! 贡献:")
        for cap_type, items in self._capabilities.items():
            for item in items: print(f"  + {cap_type}: {item}")

    def can_activate(self, event):
        return event in self._activation_on and not self._activated


class CoreEditor:
    """VS Code 核心编辑器：触发事件，调度扩展"""
    LANG_MAP = {"py": "python", "js": "javascript", "java": "java", "ts": "typescript"}

    def __init__(self):
        self._registry = ExtensionRegistry()

    def install(self, ext):
        self._registry.register(ext)

    def open_file(self, filename):
        """打开文件——触发激活事件"""
        ext = filename.split(".")[-1]
        lang = self.LANG_MAP.get(ext, ext)
        print(f"\n[CoreEditor] 打开文件: {filename} (语言: {lang})")
        self._registry.trigger_event(f"onLanguage:{lang}")

    def run_command(self, cmd_id):
        ext_name = self._registry._commands.get(cmd_id)
        if ext_name:
            print(f"[CoreEditor] 执行命令 '{cmd_id}' (由 {ext_name} 提供)")
        else:
            print(f"[CoreEditor] 命令 '{cmd_id}' 未注册")


class ExtensionRegistry:
    """扩展注册表：管理扩展、发现能力"""
    def __init__(self):
        self._extensions, self._commands, self._languages = [], {}, {}

    def register(self, ext):
        self._extensions.append(ext)
        print(f"[Registry] 发现扩展: {ext._name} (激活条件: {ext._activation_on})")

    def trigger_event(self, event):
        print(f"[Registry] 触发激活事件: {event}")
        for ext in self._extensions:
            if ext.can_activate(event):
                ext.activate()
                self._collect(ext)

    def _collect(self, ext):
        for cap_type, items in ext._capabilities.items():
            target = {"commands": self._commands, "languages": self._languages}.get(cap_type)
            if target is not None:
                for item in items: target[item] = ext._name


class PythonLintExtension(Extension):
    """Python 代码检查扩展：注册命令和语言支持"""
    def __init__(self):
        super().__init__("python-lint",
            {"commands": ["python.lint", "python.format"], "languages": ["python"]},
            ["onLanguage:python"])


if __name__ == "__main__":
    print("=" * 50)
    print("进阶演示: 模拟 VS Code 扩展系统")
    print("=" * 50 + "\n")

    editor = CoreEditor()
    editor.install(PythonLintExtension())
    editor.install(Extension("git-tools", {"commands": ["git.commit", "git.push"]}, ["onWorkspace:git"]))
    editor.install(Extension("dark-theme", {"commands": ["theme.dark"]}, ["onCommand:theme.switch"]))

    print("--- 濒加载激活演示 ---")
    editor.open_file("main.py")   # 触发 onLanguage:python → 濒加载激活
    editor.open_file("main.py")   # 已激活，不会重复

    print("\n--- 使用扩展功能 ---")
    editor.run_command("python.lint")
    editor.run_command("python.format")
    editor.run_command("git.commit")  # 未激活，命令未注册
