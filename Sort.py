'''написати функцію, яка реалізує реверсування однозв'язного списку, змінюючи посилання між вузлами;
розробити алгоритм сортування для однозв'язного списку, наприклад, сортування вставками або злиттям;
написати функцію, що об'єднує два відсортовані однозв'язні списки в один відсортований список.'''

class Node:
    """
    Клас, що представляє окремий вузол однозв'язного списку.
    Кожен вузол містить дані та посилання на наступний вузол.
    """
    def __init__(self, data=None):
        self.data = data
        self.next = None


class LinkedList:
    """
    Клас, що представляє однозв'язний список.
    Містить посилання на головний вузол (head) списку та методи для роботи зі списком.
    """
    def __init__(self):
        self.head = None

    def insert_at_beginning(self, data):
        """
        Вставляє новий вузол на початок списку.
        """
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def insert_at_end(self, data):
        """
        Вставляє новий вузол в кінець списку.
        """
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
        else:
            cur = self.head
            while cur.next:
                cur = cur.next
            cur.next = new_node

    def insert_after(self, prev_node: Node, data):
        """
        Вставляє новий вузол після заданого вузла.
        """
        if prev_node is None:
            print("Попереднього вузла не існує.")
            return
        new_node = Node(data)
        new_node.next = prev_node.next
        prev_node.next = new_node

    def delete_node(self, key: int):
        """
        Видаляє перший вузол, що містить задані дані (ключ).
        """
        cur = self.head
        # Випадок, коли потрібно видалити головний вузол
        if cur and cur.data == key:
            self.head = cur.next
            cur = None
            return
        
        prev = None
        # Пошук вузла для видалення
        while cur and cur.data != key:
            prev = cur
            cur = cur.next
        
        # Якщо вузол не знайдено
        if cur is None:
            return
        
        # Видалення вузла
        prev.next = cur.next
        cur = None

    def search_element(self, data: int) -> Node | None:
        """
        Шукає елемент у списку. Повертає вузол, якщо знайдено, інакше None.
        """
        cur = self.head
        while cur:
            if cur.data == data:
                return cur
            cur = cur.next
        return None

    def print_list(self):
        """
        Друкує всі елементи списку.
        """
        current = self.head
        while current:
            print(current.data, end=" -> ")
            current = current.next
        print("None")

    def reverse_list(self):
        """
        Реверсує однозв'язний список, змінюючи посилання між вузлами.
        """
        prev = None
        current = self.head
        while current:
            # Зберігаємо посилання на наступний вузол
            next_node = current.next
            # Змінюємо посилання поточного вузла на попередній
            current.next = prev
            # Переміщуємо 'prev' на поточний вузол
            prev = current
            # Переміщуємо 'current' на наступний вузол
            current = next_node
        # Оновлюємо голову списку на останній оброблений вузол (який став першим)
        self.head = prev

    def insertion_sort(self):
        """
        Сортує однозв'язний список за допомогою алгоритму сортування вставками.
        """
        # Якщо список порожній або має лише один елемент, він вже відсортований
        if self.head is None or self.head.next is None:
            return

        sorted_head = None  # Голова відсортованої частини списку
        current = self.head  # Починаємо з голови невідсортованої частини

        while current:
            next_node = current.next  # Зберігаємо наступний вузол
            
            # Якщо відсортована частина порожня, або поточний вузол має менші дані
            # ніж перший елемент відсортованої частини, вставляємо його на початок.
            if sorted_head is None or current.data < sorted_head.data:
                current.next = sorted_head
                sorted_head = current
            else:
                # Шукаємо правильне місце для вставки в відсортованій частині
                search_node = sorted_head
                while search_node.next and current.data > search_node.next.data:
                    search_node = search_node.next
                
                # Вставляємо поточний вузол у знайдену позицію
                current.next = search_node.next
                search_node.next = current
            
            current = next_node  # Переходимо до наступного вузла з початкового списку
        
        self.head = sorted_head # Оновлюємо голову списку на голову відсортованої частини

    @staticmethod
    def merge_sorted_lists(l1_head: Node, l2_head: Node) -> Node | None:
        """
        Об'єднує два відсортовані однозв'язні списки в один відсортований список.
        Цей метод є статичним, оскільки він не залежить від конкретного екземпляра LinkedList,
        а працює безпосередньо з головами вхідних списків.
        """
        # Створюємо фіктивний (dummy) вузол, щоб спростити логіку додавання елементів
        dummy_head = Node()
        current = dummy_head # 'current' буде вказувати на останній доданий вузол в об'єднаному списку

        l1 = l1_head
        l2 = l2_head

        # Проходимо обидва списки, порівнюючи елементи
        while l1 and l2:
            if l1.data < l2.data:
                current.next = l1
                l1 = l1.next
            else:
                current.next = l2
                l2 = l2.next
            current = current.next # Переміщуємося по об'єднаному списку

        # Додаємо залишки одного з списків, якщо вони є
        if l1:
            current.next = l1
        elif l2:
            current.next = l2

        # Повертаємо голову нового об'єднаного списку (перший елемент після фіктивного вузла)
        return dummy_head.next


# --- Приклади використання ---

print("--- Тестування базових операцій ---")
llist = LinkedList()

# Вставляємо вузли в початок
llist.insert_at_beginning(5)
llist.insert_at_beginning(10)
llist.insert_at_beginning(15)
print("Список після вставки на початок (15, 10, 5):")
llist.print_list() # Очікувано: 15 -> 10 -> 5 -> None

# Вставляємо вузли в кінець
llist.insert_at_end(20)
llist.insert_at_end(25)
print("Список після вставки в кінець (20, 25):")
llist.print_list() # Очікувано: 15 -> 10 -> 5 -> 20 -> 25 -> None

# Вставляємо вузол після існуючого
node_after_5 = llist.search_element(5)
if node_after_5:
    llist.insert_after(node_after_5, 12)
print("Список після вставки 12 після 5:")
llist.print_list() # Очікувано: 15 -> 10 -> 5 -> 12 -> 20 -> 25 -> None

# Видаляємо вузол
llist.delete_node(10)
print("\nЗв'язний список після видалення вузла з даними 10:")
llist.print_list() # Очікувано: 15 -> 5 -> 12 -> 20 -> 25 -> None

# Пошук елемента у зв'язному списку
print("\nШукаємо елемент 15:")
element = llist.search_element(15)
if element:
    print(f"Знайдено елемент: {element.data}") # Очікувано: Знайдено елемент: 15
else:
    print("Елемент не знайдено.")

print("\nШукаємо елемент 100:")
element = llist.search_element(100)
if element:
    print(f"Знайдено елемент: {element.data}")
else:
    print("Елемент не знайдено.") # Очікувано: Елемент не знайдено.

print("\n--- Тестування функції реверсування ---")
llist_reverse = LinkedList()
llist_reverse.insert_at_end(1)
llist_reverse.insert_at_end(2)
llist_reverse.insert_at_end(3)
llist_reverse.insert_at_end(4)
print("Оригінальний список для реверсування:")
llist_reverse.print_list() # Очікувано: 1 -> 2 -> 3 -> 4 -> None
llist_reverse.reverse_list()
print("Реверсований список:")
llist_reverse.print_list() # Очікувано: 4 -> 3 -> 2 -> 1 -> None

print("\n--- Тестування сортування вставками ---")
llist_sort = LinkedList()
llist_sort.insert_at_end(5)
llist_sort.insert_at_end(2)
llist_sort.insert_at_end(8)
llist_sort.insert_at_end(1)
llist_sort.insert_at_end(9)
llist_sort.insert_at_end(3)
print("Оригінальний список для сортування:")
llist_sort.print_list() # Очікувано: 5 -> 2 -> 8 -> 1 -> 9 -> 3 -> None
llist_sort.insertion_sort()
print("Відсортований список (вставками):")
llist_sort.print_list() # Очікувано: 1 -> 2 -> 3 -> 5 -> 8 -> 9 -> None

print("\n--- Тестування об'єднання відсортованих списків ---")
list1 = LinkedList()
list1.insert_at_end(1)
list1.insert_at_end(3)
list1.insert_at_end(5)
print("Список 1:")
list1.print_list() # Очікувано: 1 -> 3 -> 5 -> None

list2 = LinkedList()
list2.insert_at_end(2)
list2.insert_at_end(4)
list2.insert_at_end(6)
print("Список 2:")
list2.print_list() # Очікувано: 2 -> 4 -> 6 -> None

# Об'єднання двох списків
merged_head = LinkedList.merge_sorted_lists(list1.head, list2.head)
merged_list = LinkedList()
merged_list.head = merged_head
print("Об'єднаний відсортований список:")
merged_list.print_list() # Очікувано: 1 -> 2 -> 3 -> 4 -> 5 -> 6 -> None