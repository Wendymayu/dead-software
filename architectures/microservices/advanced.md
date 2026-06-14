# 微服务架构进阶：Kubernetes

## 软件简介

Kubernetes (K8s) 是容器编排领域的标准平台，用于自动化部署、扩缩和管理容器化应用。K8s 的控制平面本身就是微服务架构的经典案例——API Server、Controller Manager、Scheduler、etcd 各自是独立进程，通过 etcd 共享状态来协调工作。

## 该软件的架构

Kubernetes 控制平面的微服务架构：

1. **API Server**：控制平面的入口网关
   - 所有组件（包括kubectl）通过 API Server 交互
   - RESTful API，支持认证、授权、准入控制
   - 是唯一直接读写 etcd 的组件（其他组件通过 API Server 间接访问）

2. **etcd**：分布式键值存储，集群的"共享大脑"
   - 存储所有集群状态：Pod、Service、ConfigMap等
   - 提供 Watch 机制：组件可以观察特定键的变化
   - 保证强一致性（Raft 协议）
   - 是所有组件之间的"通信枢纽"

3. **Controller Manager**：观察-调和循环的核心
   - 包含多个 Controller：Deployment Controller、ReplicaSet Controller、Node Controller等
   - 每个 Controller 持续执行：观察当前状态 → 对比期望状态 → 调和差异
   - 例如：期望3个副本，实际只有2个 → Controller 创建第3个Pod

4. **Scheduler**：Pod 到 Node 的绑定决策
   - 监听未调度的 Pod（status=Pending）
   - 根据资源需求、亲和性、反亲和性等规则选择最优 Node
   - 将 Pod 绑定到 Node（写入 etcd）

**核心模式**：Watch-Reconcile Loop（观察-调和循环）
所有 Controller 的核心逻辑都是：watch etcd变化 → 比对期望vs实际 → 采取行动使实际趋向期望

## 简化实现思路

我们的简化代码模拟了 K8s 控制平面的组件协作：

- `EtcdStore` → 模拟 etcd，存储集群状态并提供 Watch 机制
- `APIServer` → 模拟 API Server，接收创建 Pod 请求并写入 etcd
- `ControllerManager` → 模拟 Controller Manager，watch etcd 变化，将 Pending Pod 推进到调度就绪状态
- `Scheduler` → 模拟 Scheduler，watch etcd 变化，为就绪 Pod 分配节点

数据流：API创建Pod → 写入etcd → Controller观察变化并调和 → Scheduler观察变化并分配节点

关键设计：所有组件通过 etcd 的 Watch 机制通信，不直接调用彼此——这正是微服务通过共享状态协调的精髓。

## 与真实实现的对照

| 简化代码 | 真实 Kubernetes | 说明 |
|---------|----------------|------|
| `EtcdStore` | etcd 分布式存储 | 真实etcd是独立集群，保证强一致性和高可用 |
| `APIServer` | kube-apiserver | 真实API Server支持REST API、认证授权、准入控制 |
| `ControllerManager` | kube-controller-manager | 真实包含数十个Controller，每个有独立的调和循环 |
| `Scheduler` | kube-scheduler | 真实Scheduler有复杂调度算法（资源、亲和性、优先级） |
| 回调式Watch | etcd Watch API | 真实etcd Watch基于gRPC流，支持历史事件回放 |
| Pending→Ready→Running | Pod生命周期 | 真实Pod有更复杂的状态机（ContainerCreating、CrashLoop等） |
| 所有组件直接读写etcd | 只有API Server读写etcd | 真实中其他组件通过API Server间接访问etcd（简化代码为突出Watch机制做了妥协） |

## 学习建议

1. **理解 Watch-Reconcile**：这是 K8s 的灵魂——不是"命令式"（"去做X"），而是"声明式"（"期望状态是X，系统自动趋向X"）
2. **思考 etcd 的角色**：etcd 是微服务间的"共享大脑"，替代了直接的服务间调用——理解这种"间接通信"模式
3. **对比命令式 vs 声明式**：传统系统"创建Pod → 启动容器"，K8s"声明需要3副本 → Controller自动维持3副本"
4. **动手实验**：用 `kubectl get events --watch` 观察一个 Pod 从创建到运行的完整事件流，体会 Watch-Reconcile 循环
5. **扩展思考**：微服务的通信模式对比——共享状态(etcd) vs 直接调用(gRPC) vs 事件总线(Pub/Sub)，各有何优劣？
