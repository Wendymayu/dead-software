"""SOA 进阶示例：模拟 Apache Camel 企业服务总线（ESB）

展示 SOA 中 ESB 的核心集成能力：
- ESB（企业服务总线）：路由消息、转换格式、协调服务
- 服务注册契约：声明接受的格式与产生的格式
- 消息在服务间流转：OrderService → ESB（路由+转换）→ PaymentService
"""


class Service:
    """SOA 服务：注册契约，通过 ESB 通信"""
    def __init__(self, name, accepts, produces):
        self._name, self._accepts, self._produces = name, accepts, produces
        self._inbox = []

    def send_to_esb(self, esb, message, target):
        print(f"[{self._name}] 发送消息到 ESB: {message} (目标: {target})")
        esb.route(message, self, target)

    def receive(self, message):
        self._inbox.append(message)
        print(f"[{self._name}] 收到消息: {message}")


class ESB:
    """企业服务总线：路由、转换、协调"""
    def __init__(self):
        self._services = {}
        self._routes = []
        self._transforms = {}

    def register(self, service):
        self._services[service._name] = service
        print(f"[ESB] 注册服务: {service._name} (接受: {service._accepts}, 产生: {service._produces})")

    def add_route(self, from_svc, to_svc):
        self._routes.append((from_svc, to_svc))
        print(f"[ESB] 配置路由: {from_svc} → {to_svc}")

    def add_transform(self, from_format, to_format, fn):
        self._transforms[(from_format, to_format)] = fn
        print(f"[ESB] 注册转换器: {from_format} → {to_format}")

    def route(self, message, sender, target):
        """路由消息：检查格式兼容性，必要时转换"""
        print(f"[ESB] 路由消息从 {sender._name} → {target}")
        target_svc = self._services[target]
        # 格式不兼容时自动转换
        if sender._produces != target_svc._accepts:
            key = (sender._produces, target_svc._accepts)
            fn = self._transforms.get(key)
            if fn:
                print(f"[ESB] 格式转换: {sender._produces} → {target_svc._accepts}")
                message = fn(message)
            else:
                print(f"[ESB] 无转换器: {key}，消息丢弃")
                return
        target_svc.receive(message)


def xml_to_json(xml_msg):
    """模拟 XML → JSON 转换"""
    items = xml_msg.replace("<order>", "").replace("</order>", "").split(",")
    pairs = [f'"field{i+1}":"{v}"' for i, v in enumerate(items)]
    return "{" + ",".join(pairs) + "}"


if __name__ == "__main__":
    print("=" * 50)
    print("进阶演示: 模拟 Apache Camel ESB SOA 架构")
    print("=" * 50 + "\n")

    esb = ESB()

    # 服务注册契约（声明接受/产生的格式）
    order_svc = Service("OrderService", "json", "xml")
    payment_svc = Service("PaymentService", "json", "json")
    notify_svc = Service("NotifyService", "json", "email")

    esb.register(order_svc)
    esb.register(payment_svc)
    esb.register(notify_svc)

    # 配置路由和格式转换
    esb.add_route("OrderService", "PaymentService")
    esb.add_route("PaymentService", "NotifyService")
    esb.add_transform("xml", "json", xml_to_json)

    # 消息流转：Order → ESB（路由+转换）→ Payment → ESB → Notify
    print("\n--- 消息流转演示 ---")
    xml_order = "<order>item=phone,qty=2,price=500</order>"
    order_svc.send_to_esb(esb, xml_order, "PaymentService")
    payment_svc.send_to_esb(esb, payment_svc._inbox[0], "NotifyService")
