"""桥接模式 (Bridge Pattern) 最小化示例

演示抽象与实现的分离：
- 抽象侧(Shape)持有实现侧(Renderer)的引用
- 新增形状不影响渲染器，新增渲染器不影响形状
- 两者独立变化，通过桥接组合
"""


from abc import ABC, abstractmethod


class Renderer(ABC):
    """实现侧：渲染器接口"""

    @abstractmethod
    def render_circle(self, radius): ...

    @abstractmethod
    def render_square(self, size): ...


class VectorRenderer(Renderer):
    """实现侧：矢量渲染"""

    def render_circle(self, radius):
        print(f"    [矢量] 绘制圆形，半径={radius}")

    def render_square(self, size):
        print(f"    [矢量] 绘制方形，边长={size}")


class RasterRenderer(Renderer):
    """实现侧：像素渲染"""

    def render_circle(self, radius):
        print(f"    [像素] 绘制圆形，半径={radius}")

    def render_square(self, size):
        print(f"    [像素] 绘制方形，边长={size}")


class Shape:
    """抽象侧：形状持有渲染器引用（桥接点）"""

    def __init__(self, renderer):
        self._renderer = renderer


class Circle(Shape):
    def __init__(self, renderer, radius):
        super().__init__(renderer)
        self._radius = radius

    def draw(self):
        print(f"[Circle] 委托渲染")
        self._renderer.render_circle(self._radius)


class Square(Shape):
    def __init__(self, renderer, size):
        super().__init__(renderer)
        self._size = size

    def draw(self):
        print(f"[Square] 委托渲染")
        self._renderer.render_square(self._size)


# --- 运行演示 ---
if __name__ == "__main__":
    print("=" * 40)
    print("桥接模式演示：形状与渲染器独立变化")
    print("=" * 40 + "\n")

    vector = VectorRenderer()
    raster = RasterRenderer()

    Circle(vector, 5).draw()
    print()
    Circle(raster, 5).draw()
    print()
    Square(vector, 3).draw()
    print()
    Square(raster, 3).draw()
