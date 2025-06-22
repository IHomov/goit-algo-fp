import uuid
import networkx as nx
import matplotlib.pyplot as plt

"""
Наступний код виконує побудову бінарних дерев.
Суть завдання полягає у створенні дерева із купи.
"""

class Node:
    def __init__(self, key, color="skyblue"):
        self.left = None
        self.right = None
        self.val = key
        self.color = color  
        self.id = str(uuid.uuid4()) 

def add_edges(graph, node, pos, x=0, y=0, layer=1):
    """
    Рекурсивно додає вузли та ребра до об'єкта графа (networkx)
    для візуалізації дерева.
    """
    if node is not None:
        graph.add_node(node.id, color=node.color, label=node.val)  # Використання id та збереження значення вузла
        if node.left:
            graph.add_edge(node.id, node.left.id)
            l = x - 1 / 2 ** layer
            pos[node.left.id] = (l, y - 1)
            add_edges(graph, node.left, pos, x=l, y=y - 1, layer=layer + 1)
        if node.right:
            graph.add_edge(node.id, node.right.id)
            r = x + 1 / 2 ** layer
            pos[node.right.id] = (r, y - 1)
            add_edges(graph, node.right, pos, x=r, y=y - 1, layer=layer + 1)
    return graph

def draw_tree(tree_root):
    """
    Відображає бінарне дерево за допомогою networkx та matplotlib.
    """
    tree = nx.DiGraph()
    pos = {tree_root.id: (0, 0)} # Початкова позиція для кореня

    # Додаємо вузли та ребра, обчислюючи їх позиції
    tree = add_edges(tree, tree_root, pos)

    # Отримуємо кольори та мітки для вузлів з графа
    colors = [node[1]['color'] for node in tree.nodes(data=True)]
    labels = {node[0]: node[1]['label'] for node in tree.nodes(data=True)}

    plt.figure(figsize=(10, 7)) # Збільшуємо розмір фігури для кращої візуалізації
    nx.draw(tree, pos=pos, labels=labels, arrows=False, node_size=3000, node_color=colors, font_size=10, font_weight="bold")
    plt.show()

# --- ФУНКЦІЯ: Побудова дерева з купи ---

def build_tree_from_heap(heap_array, index=0):
    """
    Рекурсивно будує бінарне дерево (об'єкти Node) зі списку, що представляє купу.

    heap_array (list): Список, що представляє бінарну купу.
    index (int): Поточний індекс у списку купи, з якого будуємо вузол.

    Повертає:
    Node | None: Корінь побудованого бінарного дерева або None, якщо індекс поза межами списку.
    """
    if index < len(heap_array):
        # Створюємо новий вузол для поточного елемента купи
        node = Node(heap_array[index])

        # Рекурсивно будуємо ліве дочірнє дерево
        # Лівий дочірній елемент знаходиться за індексом 2*i + 1
        node.left = build_tree_from_heap(heap_array, 2 * index + 1)

        # Рекурсивно будуємо праве дочірнє дерево
        # Правий дочірній елемент знаходиться за індексом 2*i + 2
        node.right = build_tree_from_heap(heap_array, 2 * index + 2)

        return node
    else:
        return None # Якщо індекс виходить за межі купи, повертаємо None (немає вузла)

# --- Приклад використання ---

# Приклад бінарної купи (можна уявити, що це min-heap або max-heap, для візуалізації це неважливо)
# Для min-heap: 10, 20, 30, 40, 50, 60, 70
# Для max-heap: 70, 60, 50, 40, 30, 20, 10
heap_example = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100] 

# Будуємо дерево з масиву-купи
heap_root = build_tree_from_heap(heap_example)

# Відображаємо дерево
if heap_root:
    print("Візуалізація бінарної купи:")
    draw_tree(heap_root)
else:
    print("Купа порожня, немає чого візуалізувати.")

#Оригінальний приклад для порівняння (не з купи, а довільне дерево)
print("\nВізуалізація довільного бінарного дерева (з оригінального прикладу):")
root_original = Node(0)
root_original.left = Node(4)
root_original.left.left = Node(5)
root_original.left.right = Node(10)
root_original.right = Node(1)
root_original.right.left = Node(3)
draw_tree(root_original)