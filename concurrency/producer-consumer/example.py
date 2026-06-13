"""生产者-消费者模式 最小化示例

演示队列解耦生产与消费：
- Producer 向 Queue 放入数据
- Consumer 从 Queue 取出数据
- 队列管理流量控制
"""

import threading
import queue
import time


def producer(q, count):
    """生产者：生成数据放入队列"""
    for i in range(count):
        item = f"item-{i}"
        q.put(item)
        print(f"[Producer] 放入: {item}")
        time.sleep(0.1)
    q.put(None)  # 结束信号


def consumer(q):
    """消费者：从队列取出并处理数据"""
    while True:
        item = q.get()
        if item is None:
            q.task_done()
            break
        print(f"[Consumer] 处理: {item}")
        time.sleep(0.2)
        q.task_done()


# --- 运行演示 ---
if __name__ == "__main__":
    print("=" * 40)
    print("生产者-消费者模式演示")
    print("=" * 40 + "\n")

    q = queue.Queue(maxsize=3)  # 限制队列大小，流量控制
    t_producer = threading.Thread(target=producer, args=(q, 5))
    t_consumer = threading.Thread(target=consumer, args=(q,))

    t_producer.start()
    t_consumer.start()
    t_producer.join()
    t_consumer.join()

    print("\n关键：队列解耦生产者与消费者")
    print("生产者无需知道谁消费，消费者无需知道谁生产")
