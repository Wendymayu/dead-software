"""微服务架构进阶示例：模拟 Kubernetes 控制平面

展示 K8s 各组件如何通过 etcd 协调：
API Server → etcd(共享状态) → Controller Manager(观察+调和) → Scheduler(节点分配)
每个组件是独立服务，通过共享状态存储通信。
"""


# --- etcd：共享状态存储 ---
class EtcdStore:
    """模拟 etcd：所有K8s组件通过它读写集群状态"""

    def __init__(self):
        self._data = {}
        self._watchers = []

    def put(self, key: str, value: dict):
        self._data[key] = value
        print(f"  [etcd] 写入: {key} = {value}")
        self._notify_watchers(key, value)

    def get(self, key: str) -> dict | None:
        return self._data.get(key)

    def watch(self, callback):
        """组件注册观察：当数据变化时收到通知"""
        self._watchers.append(callback)

    def _notify_watchers(self, key, value):
        for cb in self._watchers:
            cb(key, value)


# --- API Server：接收外部请求 ---
class APIServer:
    """模拟 K8s API Server：验证请求并写入etcd"""

    def __init__(self, etcd: EtcdStore):
        self.etcd = etcd

    def create_pod(self, name: str, spec: dict):
        print(f"[API Server] 收到请求: 创建Pod '{name}'")
        self.etcd.put(f"pods/{name}", {"spec": spec, "status": "Pending", "node": ""})


# --- Controller Manager：观察+调和循环 ---
class ControllerManager:
    """模拟 K8s Controller: watch etcd变化并调和期望状态"""

    def __init__(self, etcd: EtcdStore):
        self.etcd = etcd
        etcd.watch(self._on_change)

    def _on_change(self, key: str, value: dict):
        if key.startswith("pods/") and value["status"] == "Pending":
            print(f"[Controller] 检测到Pending Pod，触发调和: {key}")
            self._reconcile(key, value)

    def _reconcile(self, key: str, pod: dict):
        """调和：让Pod进入调度就绪状态"""
        pod["status"] = "ReadyForScheduling"
        self.etcd.put(key, pod)  # 更新状态回etcd


# --- Scheduler：节点分配 ---
class Scheduler:
    """模拟 K8s Scheduler：为就绪Pod分配节点"""

    def __init__(self, etcd: EtcdStore, nodes: list[str]):
        self.etcd = etcd
        self.nodes = nodes
        etcd.watch(self._on_change)

    def _on_change(self, key: str, value: dict):
        if key.startswith("pods/") and value["status"] == "ReadyForScheduling":
            print(f"[Scheduler] 为Pod分配节点: {key}")
            value["node"] = self.nodes[0]
            value["status"] = "Running"
            self.etcd.put(key, value)


if __name__ == "__main__":
    etcd = EtcdStore()
    api = APIServer(etcd)
    nodes = ["node-1", "node-2", "node-3"]

    print("=" * 50)
    print("K8s控制平面: API→etcd→Controller→Scheduler")
    print("=" * 50)

    # 先注册观察者，再创建Pod
    ControllerManager(etcd)
    Scheduler(etcd, nodes)

    print("\n--- 创建Pod ---")
    api.create_pod("web-app", {"image": "nginx", "replicas": 3})

    print("\n--- 最终状态 ---")
    pod = etcd.get("pods/web-app")
    print(f"Pod状态: {pod}")
