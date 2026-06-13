"""Reactor 模式 最小化示例

演示单线程事件循环处理多个事件源：
- EventLoop 注册 handler
- 事件多路分离后分发给对应 handler
- 单线程非阻塞处理并发
"""


class Handler:
    """事件处理器基类"""
    def handle(self, event):
        print(f"[Handler] 处理事件: {event}")


class ReadHandler(Handler):
    def handle(self, event):
        print(f"[ReadHandler] 读取: {event['data']}")


class WriteHandler(Handler):
    def handle(self, event):
        print(f"[WriteHandler] 写入: {event['data']}")


class EventLoop:
    """Reactor 核心：事件循环"""
    def __init__(self):
        self._handlers = {}
        self._events = []

    def register(self, event_type, handler):
        self._handlers[event_type] = handler

    def post(self, event):
        self._events.append(event)

    def run(self):
        """多路分离 + 分发"""
        while self._events:
            event = self._events.pop(0)
            handler = self._handlers.get(event['type'])
            if handler:
                handler.handle(event)
            else:
                print(f"[Loop] 无处理器: {event['type']}")


# --- 运行演示 ---
if __name__ == "__main__":
    print("=" * 40)
    print("Reactor 模式演示")
    print("=" * 40 + "\n")

    loop = EventLoop()
    loop.register("read", ReadHandler())
    loop.register("write", WriteHandler())

    loop.post({"type": "read", "data": "请求数据"})
    loop.post({"type": "write", "data": "响应数据"})
    loop.post({"type": "read", "data": "日志数据"})
    loop.post({"type": "unknown", "data": "未知事件"})

    loop.run()

    print("\n关键：单线程事件循环处理多种事件")
    print("注册 handler → post 事件 → 循环分发")
