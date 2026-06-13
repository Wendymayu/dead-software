"""责任链模式 (Chain of Responsibility Pattern) 最小化示例

演示请求沿处理链传递，直到被处理：
- 每个处理器判断能否处理，否则传给下一个
- 发送者无需知道哪个处理器最终处理
- 链的顺序和组成可灵活调整
"""


class Handler:
    """处理器基类：持有下一个处理者的引用"""

    def __init__(self, next_handler=None):
        self._next = next_handler

    def handle(self, request):
        """模板：先尝试自己处理，失败则传递"""
        if self._can_handle(request):
            return self._do_handle(request)
        elif self._next:
            print(f"  [{self.__class__.__name__}] 无法处理 level={request}，传递给下一个")
            return self._next.handle(request)
        else:
            print(f"  [Chain] 无人能处理 level={request}")
            return None

    def _can_handle(self, request): ...
    def _do_handle(self, request): ...


class Level1Handler(Handler):
    """一级支持：处理简单问题(level 1)"""

    def _can_handle(self, request):
        return request <= 1

    def _do_handle(self, request):
        print(f"  [Level1] 已处理 level={request} 的简单问题")
        return "Level1 解决"


class Level2Handler(Handler):
    """二级支持：处理中等问题(level 2)"""

    def _can_handle(self, request):
        return request <= 2

    def _do_handle(self, request):
        print(f"  [Level2] 已处理 level={request} 的中等问题")
        return "Level2 解决"


class Level3Handler(Handler):
    """三级支持：处理复杂问题(level 3)"""

    def _can_handle(self, request):
        return request <= 3

    def _do_handle(self, request):
        print(f"  [Level3] 已处理 level={request} 的复杂问题")
        return "Level3 解决"


# --- 运行演示 ---
if __name__ == "__main__":
    print("=" * 40)
    print("责任链模式演示：请求沿处理链传递")
    print("=" * 40 + "\n")

    # 构建链: Level1 → Level2 → Level3
    chain = Level1Handler(Level2Handler(Level3Handler()))

    print("--- 简单问题 (level=1) ---")
    chain.handle(1)
    print()

    print("--- 中等问题 (level=2) ---")
    chain.handle(2)
    print()

    print("--- 复杂问题 (level=3) ---")
    chain.handle(3)
    print()

    print("--- 超出范围 (level=4) ---")
    chain.handle(4)
