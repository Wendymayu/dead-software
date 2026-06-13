"""读写锁模式 最小化示例

演示多读者并发读 + 写者独占写：
- 多个读者可同时读取共享数据
- 写者需要独占访问，等待所有读者完成
- read_count 跟踪活跃读者数量
"""

import threading
import time


class ReadWriteLock:
    def __init__(self):
        self._read_count = 0
        self._read_lock = threading.Lock()    # 保护 read_count
        self._write_lock = threading.Lock()   # 写者独占

    def acquire_read(self):
        with self._read_lock:
            self._read_count += 1
            if self._read_count == 1:
                self._write_lock.acquire()  # 第一个读者锁住写

    def release_read(self):
        with self._read_lock:
            self._read_count -= 1
            if self._read_count == 0:
                self._write_lock.release()  # 最后一个读者释放写锁

    def acquire_write(self):
        self._write_lock.acquire()

    def release_write(self):
        self._write_lock.release()


shared_data = {"value": 0}
rw_lock = ReadWriteLock()


def reader(name):
    rw_lock.acquire_read()
    print(f"[Reader-{name}] 读取: value={shared_data['value']}")
    time.sleep(0.1)
    rw_lock.release_read()


def writer(name, new_val):
    rw_lock.acquire_write()
    shared_data["value"] = new_val
    print(f"[Writer-{name}] 写入: value={new_val}")
    time.sleep(0.1)
    rw_lock.release_write()


# --- 运行演示 ---
if __name__ == "__main__":
    print("=" * 40)
    print("读写锁模式演示")
    print("=" * 40 + "\n")

    threads = [
        threading.Thread(target=reader, args=("A",)),
        threading.Thread(target=reader, args=("B",)),
        threading.Thread(target=writer, args=("1", 10)),
        threading.Thread(target=reader, args=("C",)),
    ]

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    print(f"\n最终值: {shared_data['value']}")
    print("关键：读者并发读，写者独占写")
