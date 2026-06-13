"""Future/Promise 模式 最小化示例

演示异步计算的占位符模式：
- Future 开始时为空
- .get() 阻塞等待直到结果被设置
- 异步计算完成后设置结果
"""

import threading
import time


class Future:
    """异步结果的占位符"""
    def __init__(self):
        self._result = None
        self._done = threading.Event()

    def set(self, value):
        """计算完成，设置结果"""
        self._result = value
        self._done.set()

    def get(self):
        """阻塞等待结果"""
        self._done.wait()
        return self._result

    def is_done(self):
        return self._done.is_set()


def async_compute(future, duration):
    """模拟耗时异步计算"""
    print(f"[计算] 开始，预计 {duration}s")
    time.sleep(duration)
    result = f"计算完成(耗时{duration}s)"
    future.set(result)
    print(f"[计算] 结果已设置")


# --- 运行演示 ---
if __name__ == "__main__":
    print("=" * 40)
    print("Future/Promise 模式演示")
    print("=" * 40 + "\n")

    future = Future()
    t = threading.Thread(target=async_compute, args=(future, 0.5))
    t.start()

    print(f"[主线程] Future 完成? {future.is_done()}")
    print("[主线程] 等待结果...")
    result = future.get()
    print(f"[主线程] 拿到结果: {result}")
    print(f"[主线程] Future 完成? {future.is_done()}")

    t.join()

    print("\n关键：Future 是异步结果的占位符")
    print("调用方无需关心计算何时完成，get() 自动等待")
