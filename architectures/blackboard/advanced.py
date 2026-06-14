"""黑板架构进阶示例：Hadoop MapReduce

模拟 MapReduce 作为黑板模式：
- 输入数据分块，每个块由一个Mapper"专家"独立处理
- 中间结果写入共享黑板(模拟HDFS)
- Reducer"专家"从黑板读取并聚合，产生最终输出
- JobTracker作为控制器调度专家协作
"""


class Blackboard:
    """共享黑板：存储中间结果(模拟HDFS中间存储)"""
    def __init__(self):
        self._data = {}
        self._intermediate = {}  # key → [values]

    def write_input(self, chunk_id, data):
        self._data[chunk_id] = data
        print(f"  [黑板] 写入输入块: chunk_{chunk_id} = {data}")

    def write_intermediate(self, key, value, mapper_name):
        self._intermediate.setdefault(key, []).append(value)
        print(f"  [{mapper_name}] 写入黑板: {key} -> {value}")

    def read_intermediate(self, key):
        return self._intermediate.get(key, [])

    def get_all_keys(self):
        return list(self._intermediate.keys())

    def read_input(self, chunk_id):
        return self._data.get(chunk_id)


class MapperExpert:
    """Mapper专家：独立处理数据块，输出中间结果到黑板"""
    def __init__(self, name):
        self.name = name

    def process(self, bb, chunk_id):
        data = bb.read_input(chunk_id)
        for word in data.split():
            bb.write_intermediate(word.lower(), 1, self.name)


class ReducerExpert:
    """Reducer专家：从黑板读取中间结果，聚合产生最终输出"""
    def __init__(self, name):
        self.name = name

    def reduce(self, bb):
        results = {}
        for key in bb.get_all_keys():
            values = bb.read_intermediate(key)
            results[key] = sum(values)
            print(f"  [{self.name}] 聚合: {key} = {results[key]} (来自{len(values)}个Mapper)")
        return results


class JobTracker:
    """JobTracker控制器：调度Mapper和Reducer专家"""
    def run(self, bb, mappers, reducer, input_data):
        print("[JobTracker] Phase 1: 分块 + Map")
        for i, chunk in enumerate(input_data):
            bb.write_input(i, chunk)
            mapper = mappers[i % len(mappers)]  # 每个块分配一个Mapper
            print(f"  [JobTracker] chunk_{i} -> {mapper.name}")
            mapper.process(bb, i)
        print("\n[JobTracker] Phase 2: Shuffle + Reduce")
        return reducer.reduce(bb)


if __name__ == "__main__":
    bb = Blackboard()
    input_chunks = ["Hello World Hello", "World Hadoop Map", "Reduce Hello World"]
    mappers = [MapperExpert("Mapper-A"), MapperExpert("Mapper-B"), MapperExpert("Mapper-C")]
    reducer = ReducerExpert("Reducer-1")
    tracker = JobTracker()

    print("=" * 50)
    print("MapReduce 黑板: Mapper专家->黑板->Reducer专家")
    print("=" * 50 + "\n")

    result = tracker.run(bb, mappers, reducer, input_chunks)
    print(f"\n最终词频统计: {result}")

    print("\n--- 核心洞察 ---")
    print("  MapReduce = 黑板架构: 黑板(HDFS)=共享空间")
    print("  Mapper=独立专家写部分结果, Reducer=专家读并聚合")
    print("  JobTracker=控制器调度协作--教科书级的黑板模式应用")
