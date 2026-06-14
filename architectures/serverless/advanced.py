"""Serverless 进阶示例：模拟 AWS Lambda 函数计算平台

展示 AWS Lambda 的核心机制：
- LambdaRuntime: 注册 handler，接收事件调用
- 事件源: API Gateway(HTTP)、S3(文件)、SQS(消息)
- 冷启动 vs 热启动: 首次慢，后续快
- 函数链: Lambda A → 事件触发 → Lambda B
"""

import time


class LambdaRuntime:
    """模拟 AWS Lambda 运行时"""
    def __init__(self):
        self._funcs = {}
        self._cold = {}

    def register(self, name, handler, cold_time=0.05):
        self._funcs[name] = (handler, cold_time)
        self._cold[name] = True
        print(f"[Lambda] 注册函数: {name}")

    def invoke(self, name, event):
        handler, cold_time = self._funcs.get(name, (None, 0))
        if not handler:
            print(f"[Lambda] 404: '{name}' 未注册")
            return None
        if self._cold[name]:
            print(f"[Lambda] {name}: 冷启动 ({cold_time}s)")
            time.sleep(cold_time)
            self._cold[name] = False
        else:
            print(f"[Lambda] {name}: 热启动")
        print(f"[Lambda] {name}: 处理事件 → {event}")
        result = handler(event)
        print(f"[Lambda] {name}: 返回 {result}")
        return result


class APIGatewayEvent:
    """API Gateway 事件: HTTP 请求触发 Lambda"""
    def __init__(self, path, method="GET", body=None):
        self.path, self.method, self.body = path, method, body or {}
        print(f"  [API Gateway] {method} {path} → 触发 Lambda")

    def __repr__(self):
        return f"{self.method} {self.path}"


class S3Event:
    """S3 事件: 文件上传触发 Lambda"""
    def __init__(self, bucket, key):
        self.bucket, self.key = bucket, key
        print(f"  [S3] {bucket}/{key} 上传 → 触发 Lambda")

    def __repr__(self):
        return f"s3://{self.bucket}/{self.key}"


class SQSEvent:
    """SQS 事件: 消息队列触发 Lambda"""
    def __init__(self, message):
        self.message = message
        print(f"  [SQS] 消息: '{message}' → 触发 Lambda")

    def __repr__(self):
        return self.message


# --- Handler 函数 ---
def api_handler(event):
    return f"响应: {event.path} → {event.body}"

def s3_handler(event):
    print(f"  [handler] 处理文件 {event.key} → 发送到 SQS")
    return f"已处理 {event.key}"

def sqs_handler(event):
    return f"已消费: '{event.message}'"


if __name__ == "__main__":
    rt = LambdaRuntime()
    rt.register("api-handler", api_handler, cold_time=0.06)
    rt.register("s3-handler", s3_handler, cold_time=0.08)
    rt.register("sqs-handler", sqs_handler, cold_time=0.03)

    print("=" * 50)
    print("AWS Lambda Serverless 模拟")
    print("=" * 50 + "\n")

    print("--- API Gateway: 冷启动 → 热启动 ---")
    rt.invoke("api-handler", APIGatewayEvent("/users", "GET", {"id": 1}))
    rt.invoke("api-handler", APIGatewayEvent("/users", "GET", {"id": 2}))

    print("\n--- S3 → SQS 函数链 ---")
    rt.invoke("s3-handler", S3Event("data-bucket", "report.csv"))
    rt.invoke("sqs-handler", SQSEvent("report.csv 已处理"))
