"""微内核进阶示例：核心内进程调度 + 扩展间通信

展示微内核的进阶能力：
- 核心内提供最基础的进程调度（不是扩展）
- 扩展之间通过核心中转通信，不直接交互
- 核心比插件架构更薄——核心只做调度和最基本服务
"""


# --- 进阶微内核核心：含最基础的进程表 ---
class MicrokernelCore:
    def __init__(self):
        self._extensions = {}
        self._process_table = {}  # 核心内最基本的能力：进程管理
        self._next_pid = 1

    def register_extension(self, name, ext):
        self._extensions[name] = ext

    def create_process(self, name):
        """进程管理是核心内最基本的能力，不是扩展"""
        pid = self._next_pid
        self._next_pid += 1
        self._process_table[pid] = {"name": name, "status": "ready"}
        print(f"[Core] 创建进程 PID={pid}: {name}")
        return pid

    def list_processes(self):
        print(f"[Core] 进程表: {self._process_table}")
        return self._process_table

    def request(self, ext_name, action, params):
        ext = self._extensions.get(ext_name)
        if not ext:
            print(f"[Core] 扩展 {ext_name} 未注册")
            return None
        print(f"[Core] 调度 → {ext_name}: {action}")
        return ext.handle(action, params)

    def relay(self, from_ext, to_ext, action, params):
        """扩展之间通过核心中转——不直接通信"""
        print(f"[Core] 中转: {from_ext} → {to_ext}: {action}")
        return self.request(to_ext, action, params)


# --- 扩展 ---
class FileSystemExtension:
    def handle(self, action, params):
        print(f"  [FileSystem] 处理: {action}")
        if action == "READ":
            return {"content": f"文件 {params['path']} 的内容"}
        return {"status": "ERROR"}


class NetworkExtension:
    def handle(self, action, params):
        print(f"  [Network] 处理: {action}")
        if action == "SEND":
            print(f"    发送数据到 {params['host']}: {params['data']}")
            return {"status": "OK"}
        return {"status": "ERROR"}


class LogExtension:
    def handle(self, action, params):
        print(f"  [Log] 记录: {params.get('msg', '')}")
        return {"logged": True}


# --- 运行演示 ---
if __name__ == "__main__":
    core = MicrokernelCore()
    core.register_extension("fs", FileSystemExtension())
    core.register_extension("net", NetworkExtension())
    core.register_extension("log", LogExtension())

    print("=" * 50)
    print("进阶演示: 核心进程管理 + 扩展间中转通信")
    print("=" * 50 + "\n")

    # 核心内的进程管理（不是扩展提供的）
    pid1 = core.create_process("web-server")
    pid2 = core.create_process("db-server")
    core.list_processes()
    print()

    # 扩展间通过核心中转：fs 读文件 → net 发送
    content = core.request("fs", "READ", {"path": "/data/report"})
    print(f"  → 读取结果: {content}")
    core.relay("fs", "net", "SEND", {"host": "remote", "data": content})
    print()

    # 扩展间通过核心中转：net → log
    core.relay("net", "log", "LOG", {"msg": "数据发送完成"})
