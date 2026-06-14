"""事件溯源进阶示例：Git —— 用事件溯源管理文件版本

模拟 Git 的核心机制：
- 提交(commits)是不可变事件，存储文件变更(diff)
- 回放(replay)提交序列重建文件当前状态
- 分支(branch)是事件流的分叉，合并(merge)是事件流的汇聚
"""


class Commit:
    """不可变提交事件"""
    def __init__(self, id, diffs, parent=None, message="", branch="main"):
        self.id, self.diffs, self.parent, self.message, self.branch = id, diffs, parent, message, branch


class GitRepo:
    """Git仓库：事件存储 + 回放 + 分支 + 合并"""
    def __init__(self):
        self.commits, self.branches, self.next_id = {}, {"main": None}, 1

    def commit(self, diffs, message="", branch="main"):
        parent = self.branches[branch]
        c = Commit(self.next_id, diffs, parent, message, branch)
        self.commits[c.id] = c
        self.branches[branch] = c.id
        print(f"  [commit {c.id}] {message} (branch={branch}, parent={parent})")
        self.next_id += 1

    def replay(self, commit_id):
        """回放事件序列重建文件状态——事件溯源的核心"""
        state, chain, cid = {}, [], commit_id
        while cid is not None:
            chain.append(self.commits[cid])
            cid = self.commits[cid].parent
        for c in reversed(chain):
            for file, diff in c.diffs.items():
                if diff.startswith("+"):
                    state[file] = diff[1:]
                elif diff.startswith("-"):
                    old, new = diff[1:].split("/+")
                    state[file] = state.get(file, old).replace(old, new)
        return state

    def branch(self, name, from_branch="main"):
        self.branches[name] = self.branches[from_branch]
        print(f"  [branch] 创建 {name}, 从 {from_branch} 的 HEAD 分叉")

    def merge(self, source, target="main"):
        diffs = {f: "+" + c for f, c in self.replay(self.branches[source]).items()}
        self.commit(diffs, f"merge {source} into {target}", branch=target)


if __name__ == "__main__":
    repo = GitRepo()
    print("=" * 50)
    print("Git 事件溯源: 提交 -> 回放 -> 分支 -> 合并")
    print("=" * 50 + "\n")

    print("--- 1. 创建提交(不可变事件) ---")
    repo.commit({"readme.txt": "+Hello World"}, "初始提交")
    repo.commit({"readme.txt": "-Hello/+Hello Git", "app.py": "+print('hi')"}, "添加代码")
    print(f"  [replay] 当前状态: {repo.replay(repo.branches['main'])}\n")

    print("--- 2. 创建分支(事件流分叉) ---")
    repo.branch("feature", "main")
    repo.commit({"app.py": "-print('hi')/+print('feature')"}, "功能开发", branch="feature")
    repo.commit({"readme.txt": "-Hello Git/+Hello Git [feature]"}, "更新文档", branch="feature")
    print(f"  [replay] feature状态: {repo.replay(repo.branches['feature'])}\n")

    print("--- 3. 主分支继续演进 ---")
    repo.commit({"app.py": "-print('hi')/+print('v2')"}, "版本升级")
    print(f"  [replay] main状态: {repo.replay(repo.branches['main'])}\n")

    print("--- 4. 合并(事件流汇聚) ---")
    repo.merge("feature", "main")
    print(f"  [replay] 合并后状态: {repo.replay(repo.branches['main'])}")
    print("\n核心洞察: Git=事件溯源, commit=不可变事件, checkout=回放, branch=分叉, merge=汇聚")
