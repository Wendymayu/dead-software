"""微内核架构 (Microkernel) 最小化示例

演示最小核心 + 可选扩展：核心只提供最基本的能力，
文件系统、进程调度等都是可选扩展。与插件的区别：微内核核心更薄，扩展更基础。
"""


# --- 微内核核心：只提供最基本的服务 ---
class MicrokernelCore:
    def __init__(self):
        self._extensions = {}
        self._running = False

    def register_extension(self, name, ext):
        """核心只负责注册和调度，不关心扩展做什么"""
        self._extensions[name] = ext
        print(f"[Core] 注册扩展: {name}")

    def start(self):
        """核心启动流程——这是最小核心必须提供的"""
        self._running = True
        print("[Core] 内核启动完成")

    def request(self, ext_name, action, params):
        """核心作为调度者，将请求路由到对应扩展"""
        if not self._running:
            print("[Core] 内核未启动")
            return None
        ext = self._extensions.get(ext_name)
        if not ext:
            print(f"[Core] 扩展 {ext_name} 未注册")
            return None
        print(f"[Core] 调度 → {ext_name}: {action}")
        return ext.handle(action, params)


# --- 扩展：提供基础系统能力（不是"锦上添花"的插件，而是系统必需能力） ---
class FileSystemExtension:
    def handle(self, action, params):
        print(f"  [FileSystem] 处理: {action}")
        if action == "READ":
            return {"content": f"文件 {params['path']} 的内容"}
        if action == "WRITE":
            return {"status": "OK", "msg": f"已写入 {params['path']}"}
        return {"status": "ERROR", "msg": "不支持的操作"}


class ProcessExtension:
    def handle(self, action, params):
        print(f"  [Process] 处理: {action}")
        if action == "RUN":
            return {"pid": params.get("name", "unknown"), "status": "running"}
        return {"status": "ERROR", "msg": "不支持的操作"}


# --- 运行演示 ---
if __name__ == "__main__":
    core = MicrokernelCore()
    core.register_extension("fs", FileSystemExtension())
    core.register_extension("process", ProcessExtension())

    print("=" * 45)
    print("Microkernel 演示: 最小核心调度基本扩展")
    print("=" * 45 + "\n")

    core.start()
    print()

    r1 = core.request("fs", "READ", {"path": "/etc/config"})
    print(f"  → 结果: {r1}\n")

    r2 = core.request("process", "RUN", {"name": "server"})
    print(f"  → 结果: {r2}\n")

    # 未注册的扩展——核心只做路由，不做具体工作
    core.request("network", "CONNECT", {"host": "localhost"})
