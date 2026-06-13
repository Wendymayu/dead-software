"""适配器模式 (Adapter Pattern) 最小化示例

演示不兼容接口的桥接：
- EUPlug 只有圆脚插头，无法插入 USSocket
- USPlugAdapter 将 EUPlug 包装为 US 接口
- 适配器让已有类无需修改即可与新接口协作
"""


class EUPlug:
    """欧洲插头：圆脚，220V"""

    def connect_220v(self):
        print("[EUPlug] 圆脚插头接入 220V 电源")
        return "220V 交流电"


class USSocket:
    """美国插座：扁脚接口，110V"""

    def accept_flat_pin(self, power):
        print(f"[USSocket] 扁脚插座接收: {power}")
        return "设备通电"


class USPlugAdapter:
    """适配器：让 EUPlug 适配 USSocket 的扁脚接口"""

    def __init__(self, eu_plug):
        self._eu_plug = eu_plug
        print(f"[Adapter] 包装 {eu_plug.__class__.__name__} 为 US 接口")

    def accept_flat_pin(self, power):
        print("[Adapter] 将扁脚请求转换为圆脚请求")
        eu_power = self._eu_plug.connect_220v()
        adapted = eu_power.replace("220V", "110V(适配转换)")
        print(f"[Adapter] 适配输出: {adapted}")
        return adapted


# --- 运行演示 ---
if __name__ == "__main__":
    print("=" * 40)
    print("适配器模式演示：不兼容接口的桥接")
    print("=" * 40 + "\n")

    print("--- 不兼容情况 ---\n")
    eu_plug = EUPlug()
    us_socket = USSocket()
    print("  EUPlug 圆脚无法直接插入 USSocket 扁脚接口")
    print()

    print("--- 使用适配器 ---\n")
    adapter = USPlugAdapter(eu_plug)
    result = us_socket.accept_flat_pin(adapter.accept_flat_pin(None))
    print(f"\n  最终结果: {result}")
