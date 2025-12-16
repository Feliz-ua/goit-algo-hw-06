import networkx as nx
import matplotlib.pyplot as plt
from collections import deque

# 1. Створюємо неорієнтований граф міських доріг
G = nx.Graph()

# Перехрестя (райони міста)
nodes = [
    "Центр міста", "Залізничний Вокзал", "Мій дім", "Місце роботи",
    "Ринок", "Торгівельний центр", "Парк", "Річковий вокзал"
]
G.add_nodes_from(nodes)
# Дороги між перехрестями з «довжиною» (км)
G.add_edge("Центр міста", "Залізничний Вокзал",   weight=3)
G.add_edge("Центр міста", "Мій дім",   weight=4)
G.add_edge("Центр міста", "Місце роботи",  weight=5)
G.add_edge("Центр міста", "Ринок",     weight=2)
G.add_edge("Центр міста", "Торгівельний центр",    weight=3)
G.add_edge("Залізничний Вокзал", "Мій дім",  weight=2)
G.add_edge("Мій дім", "Ринок",    weight=3)
G.add_edge("Місце роботи", "Торгівельний центр",  weight=4)
G.add_edge("Місце роботи", "Річковий вокзал", weight=6)
G.add_edge("Ринок", "Парк",  weight=6)
G.add_edge("Торгівельний центр", "Парк", weight=8)
G.add_edge("Річковий вокзал", "Парк", weight=5)

# 2. Базові характеристики
print("Кількість вершин:", G.number_of_nodes())
print("Кількість ребер:", G.number_of_edges())

print("\nСтупені вершин:")
for node, deg in G.degree():
    print(f"{node}: {deg}")

start = "Мій дім"
goal = "Річковий вокзал"

# ---------- BFS (черга, пошук у ширину) ----------
def bfs_path(G, start, goal):
    queue = deque([[start]])
    visited = {start}
    while queue:
        path = queue.popleft()
        v = path[-1]
        if v == goal:
            return path
        for u in G.neighbors(v):
            if u not in visited:
                visited.add(u)
                queue.append(path + [u])

# ---------- DFS (стек, пошук у глибину) ----------
def dfs_path(G, start, goal):
    stack = [[start]]
    visited = {start}
    while stack:
        path = stack.pop()
        v = path[-1]
        if v == goal:
            return path
        for u in G.neighbors(v):
            if u not in visited:
                visited.add(u)
                stack.append(path + [u])

bfs_result = bfs_path(G, start, goal)
dfs_result = dfs_path(G, start, goal)

print("BFS шлях від Мого дому до Річкового вокзалу:", bfs_result)
print("DFS шлях від Мого дому до Річкового вокзалу:", dfs_result)

# --------- Дейкстра для всіх пар вершин ---------
# all_pairs_dijkstra_path повертає і довжини, і шляхи
all_shortest_paths = dict(nx.all_pairs_dijkstra_path(G, weight="weight"))
all_shortest_lengths = dict(nx.all_pairs_dijkstra_path_length(G, weight="weight"))

# Виводимо результати
for source in G.nodes():
    print(f"\nНайкоротші шляхи від '{source}':")
    for target in G.nodes():
        path = all_shortest_paths[source][target]
        dist = all_shortest_lengths[source][target]
        print(f"  до '{target}': шлях = {path}, довжина = {dist}")

# 3. Візуалізація
pos = nx.spring_layout(G, seed=42)  # зручне розташування вершин
plt.figure(figsize=(8, 6))
nx.draw(
    G, pos,
    with_labels=True,
    node_color="lightgreen",
    node_size=800,
    font_size=9,
    font_weight="bold"
)
edge_labels = nx.get_edge_attributes(G, "weight")
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)
plt.title("Транспортна мережа (NetworkX)")
plt.axis("off")
plt.show()