def greedy_algorithm(items, budget):
    """
    Жадібний алгоритм для вибору їжі.
    Обирає страви, максимізуючи співвідношення калорій до вартості.

    Аргументи:
        items (dict): Словник з інформацією про їжу (назва: {вартість, калорії}).
        budget (int): Максимально доступний бюджет.

    Повертає:
        tuple: Кортеж, що містить (обрані_страви, загальна_вартість, загальна_калорійність).
    """
    # 1. Обчислення співвідношення калорій до вартості для кожної страви
    # пошук "найвигідніші" страви
    item_ratios = {}
    for item_name, data in items.items():
        cost = data["cost"]
        calories = data["calories"]
        # Перевірка  ділення на нуль, якщо вартість 0 (хоча для їжі це не типово), але краще виконати перевірку
        ratio = calories / cost if cost > 0 else float('inf')
        item_ratios[item_name] = ratio

    # 2. Сортування страви за цим співвідношенням у спадному порядку
    # Тобто, найвигідніші страви (найбільше калорій на гривню) будуть першими. Тому що ціль, більше корисної (калорійної) їжі за меншу вартість
    sorted_items = sorted(item_ratios.items(), key=lambda item: item[1], reverse=True)

    selected_items = []
    total_cost = 0
    total_calories = 0

    # 3. Перебір відсортовані страви і додаю їх, якщо є бюджет
    for item_name, _ in sorted_items:
        cost = items[item_name]["cost"]
        calories = items[item_name]["calories"]

        if total_cost + cost <= budget:
            selected_items.append(item_name)
            total_cost += cost
            total_calories += calories
        # Якщо страва не влазить у бюджет, пропуск і пошук далі.
        # Жадібний алгоритм не повертається назад, щоб знайти кращу комбінацію!!!

    return selected_items, total_cost, total_calories


def dynamic_programming(items, budget):
    """
    Алгоритм динамічного програмування для вибору їжі.
    Знаходить оптимальний набір страв для максимізації калорійності
    при заданому бюджеті.

    Аргументи:
        items (dict): Словник з інформацією про їжу.
        budget (int): Максимально доступний бюджет.

    Повертає:
        tuple: Кортеж, що містить (обрані_страви, загальна_вартість, загальна_калорійність).
    """
    # Перетворення словник страв на список, щоб легше працювати з індексами
    item_list = [(name, data["cost"], data["calories"]) for name, data in items.items()]
    num_items = len(item_list)

    # 1. Створення таблиці для зберігання результатів проміжних розрахунків
    # dp[i][j] буде зберігати максимальну калорійність, яку можна отримати
    # з перших 'i' страв з бюджетом 'j'.
    # Рядки - це страви (від 0 до num_items)
    # Стовпці - це бюджет (від 0 до budget)
    dp = [[0 for _ in range(budget + 1)] for _ in range(num_items + 1)]

    # 2. Заповнення таблиці
    # Проходження по кожній страві
    for i in range(1, num_items + 1):
        item_name, cost, calories = item_list[i-1] # item_list індексується з 0, dp з 1

        # Проходження по кожному можливому бюджету
        for j in range(budget + 1):
            # Варіант 1: Не беремо поточну страву
            # Калорійність така ж, як і без неї (dp[i-1][j])
            dp[i][j] = dp[i-1][j]

            # Варіант 2: Можемо взяти поточну страву
            # Якщо поточна вартість (cost) не перевищує поточний бюджет (j)
            if j >= cost:
                # Обираємо кращий варіант:
                # 1. Не беремо поточну страву (dp[i-1][j])
                # 2. Беремо поточну страву: калорійність поточної страви (calories)
                #    плюс максимальна калорійність, яку ми могли отримати
                #    з попередніх страв, використовуючи залишок бюджету (j - cost).
                dp[i][j] = max(dp[i][j], calories + dp[i-1][j-cost])

    # 3. Відновлення обраних страв, використовуючи заповнену таблицю dp
    selected_items = []
    current_cost = budget
    # Починаю з останньої клітинки таблиці (максимальна калорійність з усього бюджету)
    # та рухаюсь "назад", щоб визначити, які страви були обрані(на відміну від жадібного алгоритму!).
    for i in range(num_items, 0, -1): # Йду від останньої страви до першої
        item_name, cost, calories = item_list[i-1]

        # Якщо значення в поточній клітинці відрізняється від значення в клітинці
        # без цієї страви (тобто, dp[i-1][current_cost]),
        # це означає, що поточна страва була включена в оптимальне рішення.
        if dp[i][current_cost] != dp[i-1][current_cost]:
            selected_items.append(item_name)
            current_cost -= cost # Зменшую бюджет на вартість обраної страви

    # Оскільки було переглянути список назад, список selected_items буде у зворотному порядку.
    selected_items.reverse() # треба поверрнути його в нормальний порядок

    final_total_calories = dp[num_items][budget]
    final_total_cost = 0
    for item_name in selected_items:
        final_total_cost += items[item_name]["cost"]


    return selected_items, final_total_cost, final_total_calories


# --- Приклад використання ---
items = {
    "pizza": {"cost": 50, "calories": 300},
    "hamburger": {"cost": 40, "calories": 250},
    "hot-dog": {"cost": 30, "calories": 200},
    "pepsi": {"cost": 10, "calories": 100},
    "cola": {"cost": 15, "calories": 220},
    "potato": {"cost": 25, "calories": 350}
}

budget = 100

print(f"Доступні страви: {items}")
print(f"Бюджет: {budget}\n")

# Виклик жадібного алгоритму
greedy_selected, greedy_cost, greedy_calories = greedy_algorithm(items, budget)
print("--- Жадібний алгоритм ---")
print(f"Обрані страви: {greedy_selected}")
print(f"Загальна вартість: {greedy_cost}")
print(f"Загальна калорійність: {greedy_calories}\n")

# Виклик алгоритму динамічного програмування
dp_selected, dp_cost, dp_calories = dynamic_programming(items, budget)
print("--- Динамічне програмування ---")
print(f"Обрані страви: {dp_selected}")
print(f"Загальна вартість: {dp_cost}")
print(f"Загальна калорійність: {dp_calories}\n")

# Додатковий приклад з іншим бюджетом
budget_2 = 75
print(f"--- Приклад з бюджетом {budget_2} ---")
greedy_selected_2, greedy_cost_2, greedy_calories_2 = greedy_algorithm(items, budget_2)
print("Жадібний алгоритм:")
print(f"  Обрані страви: {greedy_selected_2}")
print(f"  Загальна вартість: {greedy_cost_2}")
print(f"  Загальна калорійність: {greedy_calories_2}")

dp_selected_2, dp_cost_2, dp_calories_2 = dynamic_programming(items, budget_2)
print("Динамічне програмування:")
print(f"  Обрані страви: {dp_selected_2}")
print(f"  Загальна вартість: {dp_cost_2}")
print(f"  Загальна калорійність: {dp_calories_2}")