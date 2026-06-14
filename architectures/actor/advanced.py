"""Actor 进阶示例：模拟 Akka Actor 系统（含监督者）
展示 Akka 的核心 Actor 架构：
- ActorRef：可寻址引用，只能通过它发消息（不暴露内部）
- Mailbox：每个 Actor 有自己的消息队列，逐条处理
- SupervisorActor：监督子 Actor，失败时自动重启（"让它崩溃"哲学）
- WorkerActor：接收任务并发送结果，模拟崩溃
"""


class ActorRef:
    """ActorRef：对 Actor 的地址引用"""
    def __init__(self, name, actor, system):
        self._name, self._actor, self._system = name, actor, system
    def tell(self, message, sender=None):
        src = sender._name if sender else "system"
        print(f"[→ {self._name}] 消息: {message} (来自 {src})")
        self._actor._mailbox.append((message, sender))


class Actor:
    """Actor 基类：邮箱队列，逐条处理"""
    def __init__(self):
        self._mailbox, self._ref = [], None
    def receive(self, message, sender): pass
    def process_mailbox(self):
        while self._mailbox: msg, sender = self._mailbox.pop(0); self.receive(msg, sender)


class ActorSystem:
    """ActorSystem：管理 Actor 生命周期"""
    def __init__(self, name):
        self._name, self._actors = name, {}
        print(f"[ActorSystem:{name}] 系统启动")
    def actor_of(self, cls, name):
        actor = cls(); ref = ActorRef(name, actor, self)
        actor._ref = ref; self._actors[name] = ref
        print(f"[ActorSystem] 创建 Actor: {name}"); return ref
    def restart(self, name, cls):
        print(f"[ActorSystem] 重启 Actor: {name} (监督者策略)")
        actor = cls(); ref = ActorRef(name, actor, self)
        actor._ref = ref; self._actors[name] = ref; return ref
    def run(self):
        for ref in list(self._actors.values()): ref._actor.process_mailbox()


class SupervisorActor(Actor):
    """监督者 Actor：监控 Worker，处理失败"""
    def receive(self, message, sender):
        if message == "spawn-workers":
            print("  [Supervisor] 创建 Worker Actors")
            self._w1 = self._ref._system.actor_of(WorkerActor, "worker-1")
            self._w2 = self._ref._system.actor_of(WorkerActor, "worker-2")
            self._w1._actor._supervisor = self._ref
            self._w2._actor._supervisor = self._ref
        elif message == "task":
            print("  [Supervisor] 分发任务到 Worker-1")
            self._w1.tell("compute:42", self._ref)
        elif message.startswith("failed:"):
            wn = message.split(":")[1]
            print(f"  [Supervisor] Worker {wn} 崩溃! 执行重启策略")
            self._ref._system.restart(wn, WorkerActor)
        elif message.startswith("done:"):
            print(f"  [Supervisor] 任务完成: {message}")


class WorkerActor(Actor):
    """Worker Actor：处理任务，模拟可能崩溃"""
    _fail_on = "compute:FAIL"
    def receive(self, message, sender):
        if message == self._fail_on:
            print(f"  [Worker] 处理 '{message}' → 崩溃!")
            if hasattr(self, '_supervisor') and self._supervisor:
                self._supervisor.tell(f"failed:{self._ref._name}")
        else:
            print(f"  [Worker] 处理任务: {message} → 完成")
            if sender: sender.tell(f"done:{message}", self._ref)


if __name__ == "__main__":
    system = ActorSystem("akka-demo")
    print("=" * 50)
    print("进阶演示: 模拟 Akka Actor 系统（含监督者）")
    print("=" * 50 + "\n")
    supervisor = system.actor_of(SupervisorActor, "supervisor")

    print("--- 1. 监督者创建 Worker Actors ---")
    supervisor.tell("spawn-workers"); system.run()

    print("\n--- 2. 正常任务：Worker 处理成功 ---")
    supervisor.tell("task"); system.run()

    print("\n--- 3. 模拟崩溃：Worker 收到失败任务 ---")
    system._actors["worker-1"].tell("compute:FAIL", supervisor); system.run()

    print("\n--- 4. 重启后恢复正常 ---")
    supervisor._w1 = system._actors["worker-1"]
    supervisor.tell("task"); system.run()

    print("\n[关键] 无共享状态，所有通信通过消息，崩溃由监督者处理")
