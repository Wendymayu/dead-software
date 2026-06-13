"""组合模式 (Composite Pattern) 最小化示例

演示树形结构的统一处理：
- 叶子(Leaf)和组合(Composite)实现同一接口
- 组合对象递归管理子对象
- 客户端无需区分叶子还是组合，统一调用
"""


class FileSystemNode:
    """统一接口：文件和文件夹都有 get_size()"""

    def get_size(self):
        ...


class File(FileSystemNode):
    """叶子：没有子对象，直接返回自身大小"""

    def __init__(self, name, size):
        self._name = name
        self._size = size

    def get_size(self):
        print(f"    [File] {self._name}: {self._size}KB")
        return self._size


class Folder(FileSystemNode):
    """组合：递归汇总所有子对象的大小"""

    def __init__(self, name):
        self._name = name
        self._children = []

    def add(self, node):
        self._children.append(node)

    def get_size(self):
        total = sum(child.get_size() for child in self._children)
        print(f"  [Folder] {self._name}: {total}KB")
        return total


# --- 运行演示 ---
if __name__ == "__main__":
    print("=" * 40)
    print("组合模式演示：文件与文件夹统一计算大小")
    print("=" * 40 + "\n")

    # 构建树形结构
    readme = File("readme.txt", 2)
    src_a = File("a.py", 10)
    src_b = File("b.py", 20)
    test_c = File("c_test.py", 5)

    src_folder = Folder("src")
    src_folder.add(src_a)
    src_folder.add(src_b)

    test_folder = Folder("tests")
    test_folder.add(test_c)

    project = Folder("project")
    project.add(readme)
    project.add(src_folder)
    project.add(test_folder)

    print("--- 递归计算 project 总大小 ---\n")
    total = project.get_size()
    print(f"\n总大小: {total}KB")
