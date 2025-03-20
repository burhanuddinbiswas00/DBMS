from collections import defaultdict

class DeadlockDetector:
    def __init__(self):
        self.graph = defaultdict(list)  # Wait-for graph

    def add_edge(self, from_tx, to_tx):
        self.graph[from_tx].append(to_tx)

    def detect_cycle(self):
        visited = set()
        recursion_stack = set()

        def dfs(node):
            if node in recursion_stack:
                return True  # Cycle detected
            if node in visited:
                return False

            visited.add(node)
            recursion_stack.add(node)

            for neighbor in self.graph[node]:
                if dfs(neighbor):
                    return True

            recursion_stack.remove(node)
            return False

        for node in list(self.graph):
            if dfs(node):
                return True  # Cycle detected

        return False  # No cycle
