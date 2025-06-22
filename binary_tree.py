import uuid
import networkx as nx
import matplotlib.pyplot as plt
from collections import deque
import time

class Node:
    def __init__(self, key, color="skyblue"):
        self.left = None
        self.right = None
        self.val = key
        self.color = color
        self.id = str(uuid.uuid4())

    def deepcopy(self):
        new_node = Node(self.val, self.color)
        new_node.id = self.id
        if self.left:
            new_node.left = self.left.deepcopy()
        if self.right:
            new_node.right = self.right.deepcopy()
        return new_node


def add_edges(graph, node, pos, x=0, y=0, layer=1):
    """
    Рекурсивно додає вузли та ребра до об'єкта графа (networkx)
    та обчислює їхні позиції.
    Ця функція призначена для первинного обчислення позицій
    для всієї структури дерева.
    """
    if node is not None:
        graph.add_node(node.id, color=node.color, label=node.val)
        pos[node.id] = (x, y)

        if node.left:
            graph.add_edge(node.id, node.left.id)
            l = x - 1 / 2 ** layer
            add_edges(graph, node.left, pos, x=l, y=y - 1, layer=layer + 1)
        if node.right:
            graph.add_edge(node.id, node.right.id)
            r = x + 1 / 2 ** layer
            add_edges(graph, node.right, pos, x=r, y=y - 1, layer=layer + 1)
    return graph


def draw_tree_step(tree_root_current_state, fixed_pos, figure, ax, title="Візуалізація Обходу Дерева"):
    """
    Оновлює існуючий графік для візуалізації дерева на кожному кроці.
    """
    ax.clear()
    ax.set_title(title)

    if tree_root_current_state is None:
        ax.text(0.5, 0.5, "Дерево порожнє", horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
        figure.canvas.draw_idle()
        figure.canvas.flush_events()
        return

    current_frame_graph = nx.DiGraph()
    
    stack_dfs = [tree_root_current_state]
    visited_ids = set()

    nodes_for_drawing = []
    edges_for_drawing = []

    while stack_dfs:
        node = stack_dfs.pop()
        if node.id in visited_ids:
            continue
        visited_ids.add(node.id)

        nodes_for_drawing.append((node.id, {'color': node.color, 'label': node.val}))
        
        if node.left:
            edges_for_drawing.append((node.id, node.left.id))
            stack_dfs.append(node.left)
        if node.right:
            edges_for_drawing.append((node.id, node.right.id))
            stack_dfs.append(node.right)
            
    current_frame_graph.add_nodes_from(nodes_for_drawing)
    current_frame_graph.add_edges_from(edges_for_drawing)

    colors = [node[1]['color'] for node in current_frame_graph.nodes(data=True)]
    labels = {node[0]: node[1]['label'] for node in current_frame_graph.nodes(data=True)}

    nx.draw(current_frame_graph, pos=fixed_pos, labels=labels, arrows=False, node_size=3000,
            node_color=colors, font_size=10, font_weight="bold", ax=ax)

    figure.canvas.draw_idle()
    figure.canvas.flush_events()

# --- Функція для генерації кольорів ---
def get_color_from_step(step, total_steps):
    if total_steps == 0:
        return "#000000"

    normalized_step = step / total_steps

    r_val = int(20 + 200 * normalized_step)
    g_val = int(50 + 200 * normalized_step)
    b_val = int(100 + 150 * normalized_step)

    r_val = min(255, max(0, r_val))
    g_val = min(255, max(0, g_val))
    b_val = min(255, max(0, b_val))

    return f"#{r_val:02x}{g_val:02x}{b_val:02x}"

# --- Обхід у ширину (BFS) ---
def bfs_traverse_and_visualize(root_node, initial_pos, figure, ax):
    """
    Виконує обхід дерева в ширину (BFS) та візуалізує кожен крок
    вже на існуючому вікні matplotlib.
    """
    if root_node is None:
        return

    tree_copy = root_node.deepcopy()
    queue = deque([tree_copy])
    visited_nodes_count = 0

    total_nodes = 0
    temp_q = deque([tree_copy])
    while temp_q:
        node = temp_q.popleft()
        total_nodes += 1
        if node.left:
            temp_q.append(node.left)
        if node.right:
            temp_q.append(node.right)

    print("\n--- Візуалізація Обходу в Ширину (BFS) ---")
    while queue:
        current_node = queue.popleft()
        
        visited_nodes_count += 1
        current_node.color = get_color_from_step(visited_nodes_count, total_nodes)
        
        draw_tree_step(tree_copy, initial_pos, figure, ax, title=f"BFS: Крок {visited_nodes_count} (Вузол {current_node.val})")
        time.sleep(0.8)

        if current_node.left:
            queue.append(current_node.left)
        if current_node.right:
            queue.append(current_node.right)
    
    # Фінальний кадр BFS
    draw_tree_step(tree_copy, initial_pos, figure, ax, title="BFS: Завершено")
    time.sleep(2)

# --- Обхід у глибину (DFS) ---
def dfs_traverse_and_visualize(root_node, initial_pos, figure, ax):
    """
    Виконує обхід дерева в глибину (DFS) та візуалізує кожен крок
    вже на існуючому вікні matplotlib.
"""
    if root_node is None:
        return

    tree_copy = root_node.deepcopy()
    stack = [tree_copy]
    visited_nodes_count = 0

    total_nodes = 0
    temp_q = deque([tree_copy])
    while temp_q:
        node = temp_q.popleft()
        total_nodes += 1
        if node.left:
            temp_q.append(node.left)
        if node.right:
            temp_q.append(node.right)

    print("\n--- Візуалізація Обходу в Глибину (DFS) ---")
    while stack:
        current_node = stack.pop()
        
        visited_nodes_count += 1
        current_node.color = get_color_from_step(visited_nodes_count, total_nodes)
        
        draw_tree_step(tree_copy, initial_pos, figure, ax, title=f"DFS: Крок {visited_nodes_count} (Вузол {current_node.val})")
        time.sleep(0.8)

        if current_node.right:
            stack.append(current_node.right)
        if current_node.left:
            stack.append(current_node.left)
    
    # Фінальний кадр DFS
    draw_tree_step(tree_copy, initial_pos, figure, ax, title="DFS: Завершено")
    time.sleep(2)


# --- Створення тестового дерева ---
root = Node(0)
root.left = Node(4)
root.left.left = Node(5)
root.left.right = Node(10)
root.right = Node(1)
root.right.left = Node(3)
root.right.right = Node(8)
root.left.left.left = Node(9)
root.left.left.right = Node(2)


# --- Основна логіка запуску ---
if __name__ == "__main__":
    plt.ion() # Включаємо інтерактивний режим Matplotlib
    figure, ax = plt.subplots(figsize=(10, 7)) # Створюємо фігуру та осі один раз

    initial_graph_structure = nx.DiGraph()
    initial_pos = {}
    add_edges(initial_graph_structure, root, initial_pos) # Заповнюємо initial_pos

    print("Початковий стан дерева:")
    draw_tree_step(root, initial_pos, figure, ax, title="Початковий стан дерева")
    time.sleep(1.5)

    bfs_traverse_and_visualize(root, initial_pos, figure, ax)

    print("\nПідготовка до DFS...")
    draw_tree_step(root, initial_pos, figure, ax, title="Дерево для DFS (початковий стан)")
    time.sleep(1.5)

    dfs_traverse_and_visualize(root, initial_pos, figure, ax)

    # --- ЗАЛИШАЄМО ВІКНО ВІДКРИТИМ, ДОКИ КОРИСТУВАЧ ЙОГО НЕ ЗАКРИЄ ---
    print("\nВізуалізація завершена. Будь ласка, закрийте вікно вручну.")
    plt.ioff() # Вимикаємо інтерактивний режим перед plt.show(block=True)
    plt.show(block=True) # Блокуємо виконання, доки вікно не закриється