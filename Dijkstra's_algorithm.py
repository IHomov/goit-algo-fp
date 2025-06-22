import heapq # модуль для роботи з купами

def dijkstra_with_heap(graph, start):
    """
    Знаходить найкоротші шляхи від початкової вершини до всіх інших
    у зваженому графі за допомогою алгоритму Дейкстри з бінарною купою (heapq).

    Повертає:
    dict: Словник з найкоротшими відстанями від стартової вершини до кожної іншої.
    """

    # 1. Ініціалізація відстаней
    distances = {vertex: float('infinity') for vertex in graph}
    distances[start] = 0

    # 2. Створення пріоритетної черги (бінарної купи)
    priority_queue = [(0, start)] # Кортеж (відстань, вершина)

    # 3. Основний цикл алгоритму
    
    while priority_queue:
        current_distance, current_vertex = heapq.heappop(priority_queue)
        if current_distance > distances[current_vertex]:
            continue

        # 4. Перебираємо всіх сусідів поточної вершини
        for neighbor, weight in graph[current_vertex].items():
            # Обчислюємо нову відстань до сусіда через поточну вершину
            distance = current_distance + weight

            # 5. Оновлення найкоротшого шляху, якщо знайдено коротший
            if distance < distances[neighbor]:
                distances[neighbor] = distance # Оновлюємо відстань
                # Додаємо сусіда в пріоритетну чергу з оновленою відстанню.
                # heapq.heappush() додає елемент в купу, підтримуючи її властивості.
                heapq.heappush(priority_queue, (distance, neighbor))

    return distances

# --- Приклад використання ---

# Граф у вигляді словника
graph = {
    'A': {'B': 5, 'C': 10},
    'B': {'A': 5, 'D': 3},
    'C': {'A': 10, 'D': 2},
    'D': {'B': 3, 'C': 2, 'E': 4},
    'E': {'D': 4}
}

print("Найкоротші шляхи від 'A':")
print(dijkstra_with_heap(graph, 'A'))

print("\nНайкоротші шляхи від 'D':")
graph_from_D = {
    'A': {'B': 5, 'C': 10},
    'B': {'A': 5, 'D': 3},
    'C': {'A': 10, 'D': 2},
    'D': {'B': 3, 'C': 2, 'E': 4},
    'E': {'D': 4}
}
print(dijkstra_with_heap(graph_from_D, 'D'))
