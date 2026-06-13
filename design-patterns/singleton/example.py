"""单例模式 (Singleton Pattern) 最小化示例

演示全局唯一实例的保证：
- Config 类确保只有一个实例存在
- 展示线程安全的基本实现
- 说明单例模式的争议性
"""


class Config:
    """单例：全局配置，确保唯一实例"""

    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            print("[Config] 创建唯一实例 (首次)")
            cls._instance = super().__new__(cls)
        else:
            print("[Config] 返回已有实例 (非首次)")
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self.settings = {"theme": "dark", "lang": "zh"}
            self._initialized = True
            print("[Config] 初始化配置")

    def set(self, key, value):
        self.settings[key] = value
        print(f"[Config] 设置 {key}={value}")

    def get(self, key):
        return self.settings.get(key)


def show_controversy():
    """单例模式的争议：全局状态与隐藏依赖"""
    print("\n--- 单例模式的争议 ---")
    print("[争议1] 全局状态——任何地方都能修改，调试困难")
    print("[争议2] 隐藏依赖——函数不声明依赖 Config，但内部偷偷用")
    print("[争议3] 测试困难——无法轻松替换 mock 实例")
    print("[建议] Python 中优先用模块级变量或依赖注入代替单例")


# --- 运行演示 ---
if __name__ == "__main__":
    print("=" * 40)
    print("单例模式演示：全局唯一实例")
    print("=" * 40 + "\n")

    print("--- 创建两个 Config 实例 ---\n")
    config_a = Config()
    config_b = Config()
    print(f"  config_a is config_b? {config_a is config_b}")
    print()

    print("--- 全局共享状态 ---\n")
    config_a.set("theme", "light")
    print(f"  config_b.get('theme') = {config_b.get('theme')}")
    print(f"  同一实例? {config_a is config_b}")

    show_controversy()
