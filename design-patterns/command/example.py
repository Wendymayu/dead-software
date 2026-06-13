"""命令模式 (Command Pattern) 最小化示例

演示将操作封装为对象：
- RemoteControl 存储 Command 对象
- 命令可以执行和撤销
- 解耦请求发送者与接收者
"""


class Command:
    def execute(self): ...
    def undo(self): ...


class LightOn(Command):
    def __init__(self, light): self._light = light
    def execute(self): self._light.on()
    def undo(self): self._light.off()


class LightOff(Command):
    def __init__(self, light): self._light = light
    def execute(self): self._light.off()
    def undo(self): self._light.on()


class VolumeUp(Command):
    def __init__(self, tv): self._tv = tv
    def execute(self): self._tv.volume_up()
    def undo(self): self._tv.volume_down()


class Light:
    def on(self): print("[Light] 灯已打开")
    def off(self): print("[Light] 灯已关闭")


class TV:
    _volume = 5
    def volume_up(self):
        self._volume += 1
        print(f"[TV] 音量增大: {self._volume}")
    def volume_down(self):
        self._volume -= 1
        print(f"[TV] 音量减小: {self._volume}")


class RemoteControl:
    """遥控器：命令调用者，支持撤销"""

    def __init__(self): self._history = []

    def press(self, command):
        print(f"[Remote] 执行: {command.__class__.__name__}")
        command.execute()
        self._history.append(command)

    def undo(self):
        if not self._history:
            print("[Remote] 无可撤销命令"); return
        cmd = self._history.pop()
        print(f"[Remote] 撤销: {cmd.__class__.__name__}")
        cmd.undo()


# --- 运行演示 ---
if __name__ == "__main__":
    print("=" * 40)
    print("命令模式演示：操作封装为对象，支持撤销")
    print("=" * 40 + "\n")
    light, tv, remote = Light(), TV(), RemoteControl()
    print("--- 执行命令 ---\n")
    remote.press(LightOn(light))
    remote.press(VolumeUp(tv))
    remote.press(LightOff(light))
    print()
    print("--- 撤销命令 ---\n")
    remote.undo()
    remote.undo()
