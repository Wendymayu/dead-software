"""事件驱动架构进阶示例：模拟 Redis Pub/Sub

展示 Redis 发布订阅的核心机制：
- 频道订阅与消息发布
- 多订阅者接收同一频道消息
- 模式订阅(PATTERN)支持通配符匹配
"""


# --- Redis Pub/Sub 实现 ---
class RedisPubSub:
    """模拟 Redis Pub/Sub：频道订阅 + 模式订阅"""

    def __init__(self):
        self._channels = {}   # channel -> [subscriber_callbacks]
        self._patterns = []   # [(pattern, callback)]

    def subscribe(self, channel: str, callback):
        """订阅指定频道（精确匹配）"""
        if channel not in self._channels:
            self._channels[channel] = []
        self._channels[channel].append(callback)
        print(f"[SUBSCRIBE] 订阅频道: {channel}")

    def psubscribe(self, pattern: str, callback):
        """模式订阅（通配符匹配：* 匹配任意段）"""
        self._patterns.append((pattern, callback))
        print(f"[PSUBSCRIBE] 模式订阅: {pattern}")

    def publish(self, channel: str, message: str):
        """发布消息：先匹配精确频道，再匹配模式订阅"""
        print(f"[PUBLISH] 频道={channel} 消息='{message}'")
        count = 0
        # 精确频道订阅者
        for cb in self._channels.get(channel, []):
            cb(channel, message)
            count += 1
        # 模式订阅匹配
        for pattern, cb in self._patterns:
            if self._match_pattern(pattern, channel):
                cb(pattern, channel, message)
                count += 1
        print(f"  → 共 {count} 个订阅者收到消息")

    def _match_pattern(self, pattern: str, channel: str) -> bool:
        """简单通配符：* 匹配任意字符"""
        import fnmatch
        return fnmatch.fnmatch(channel, pattern)


# --- 订阅者回调 ---
def log_subscriber(channel: str, message: str):
    print(f"  [日志订阅者] 频道={channel} 消息='{message}'")

def alert_subscriber(channel: str, message: str):
    print(f"  [告警订阅者] 频道={channel} 消息='{message}'")

def pattern_sub(pattern: str, channel: str, message: str):
    print(f"  [模式订阅者] 匹配={pattern} 实际频道={channel} 消息='{message}'")


if __name__ == "__main__":
    redis = RedisPubSub()

    print("=" * 50)
    print("Redis Pub/Sub: 频道订阅 + 模式订阅")
    print("=" * 50 + "\n")

    # 精确订阅
    print("--- 精确订阅 ---")
    redis.subscribe("news.tech", log_subscriber)
    redis.subscribe("news.tech", alert_subscriber)
    redis.subscribe("news.sports", log_subscriber)

    # 模式订阅
    print("\n--- 模式订阅 ---")
    redis.psubscribe("news.*", pattern_sub)
    redis.psubscribe("alert.*", pattern_sub)

    # 发布消息
    print("\n--- 发布到 news.tech ---")
    redis.publish("news.tech", "新框架发布v2.0")

    print("\n--- 发布到 news.sports ---")
    redis.publish("news.sports", "中国队获胜")

    print("\n--- 发布到 alert.cpu ---")
    redis.publish("alert.cpu", "CPU使用率超过90%")
