"""策略模式 (Strategy Pattern) 最小化示例

演示算法族的封装与互换：
- 不同策略实现同一接口
- 上下文对象可以在运行时切换策略
- 新增策略无需修改已有代码
"""

from abc import ABC, abstractmethod


class SortStrategy(ABC):
    @abstractmethod
    def sort(self, data): ...


class BubbleSort(SortStrategy):
    def sort(self, data):
        print("    [策略] 使用冒泡排序")
        arr = list(data)
        n = len(arr)
        for i in range(n):
            for j in range(0, n - i - 1):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
        return arr


class QuickSort(SortStrategy):
    def sort(self, data):
        print("    [策略] 使用快速排序")
        if len(data) <= 1:
            return list(data)
        pivot = data[len(data) // 2]
        left = [x for x in data if x < pivot]
        middle = [x for x in data if x == pivot]
        right = [x for x in data if x > pivot]
        return self.sort(left) + middle + self.sort(right)


class BuiltInSort(SortStrategy):
    def sort(self, data):
        print("    [策略] 使用内置排序")
        return sorted(data)


class Sorter:
    """上下文：持有一个策略，可在运行时切换"""

    def __init__(self, strategy=None):
        self._strategy = strategy or BuiltInSort()

    def set_strategy(self, strategy):
        print(f"[Sorter] 切换策略为: {strategy.__class__.__name__}")
        self._strategy = strategy

    def sort(self, data):
        print(f"[Sorter] 排序 {data}")
        result = self._strategy.sort(data)
        print(f"[Sorter] 结果: {result}")
        return result


# --- 运行演示 ---
if __name__ == "__main__":
    print("=" * 40)
    print("策略模式演示：运行时切换排序算法")
    print("=" * 40 + "\n")

    data = [5, 3, 8, 1, 9, 2, 7]
    sorter = Sorter()

    sorter.sort(data)
    print()

    sorter.set_strategy(BubbleSort())
    sorter.sort(data)
    print()

    sorter.set_strategy(QuickSort())
    sorter.sort(data)
