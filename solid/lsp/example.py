"""里氏替换原则 (LSP) 最小化示例

演示 Square 继承 Rectangle 导致行为异常：
- Rectangle 的 width/height 独立设置
- Square 设置 width 时自动修改 height，违反预期
- 子类不能替换父类而不破坏程序行为
"""


class Rectangle:
    def __init__(self, w, h):
        self._width = w
        self._height = h

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._width = value

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = value

    def area(self):
        return self._width * self._height


class Square(Rectangle):
    """Square 继承 Rectangle，但强制边长相等"""
    @Rectangle.width.setter
    def width(self, value):
        self._width = value
        self._height = value  # 违反预期：设宽度也改了高度

    @Rectangle.height.setter
    def height(self, value):
        self._width = value  # 违反预期：设高度也改了宽度
        self._height = value


def use_rectangle(rect):
    """期望：设置 width=4, height=5 → area=20"""
    rect.width = 4
    rect.height = 5
    area = rect.area()
    expected = 4 * 5
    ok = area == expected
    print(f"  area={area}, expected={expected}, 行为正常={ok}")


# --- 运行演示 ---
if __name__ == "__main__":
    print("=" * 40)
    print("LSP 演示：里氏替换原则")
    print("=" * 40 + "\n")

    print("--- Rectangle (行为正常) ---")
    use_rectangle(Rectangle(2, 3))
    print()

    print("--- Square (违反 LSP) ---")
    use_rectangle(Square(2, 2))
    print()

    print("关键区别：Square 不能替换 Rectangle")
    print("设 width=4 后再设 height=5，Square 面积=25≠20")
    print("子类行为与父类契约不一致 → 违反 LSP")
