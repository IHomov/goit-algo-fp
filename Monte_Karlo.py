import random
from collections import Counter
import matplotlib.pyplot as plt
import pandas as pd # Для зручного відображення таблиць

def monte_carlo_dice_roll(num_simulations):
    """
    Імітує кидання двох гральних кубиків велику кількість разів
    і обчислює суми та їх частоти.

    Args:
        num_simulations (int): Кількість імітацій кидків кубиків.

    Returns:
        tuple: Кортеж, що містить:
               - dict: Словник з частотами кожної суми.
               - int: Загальна кількість симуляцій.
    """
    sums = []
    for _ in range(num_simulations):
        die1 = random.randint(1, 6) # Кидаємо перший кубик
        die2 = random.randint(1, 6) # Кидаємо другий кубик
        sums.append(die1 + die2)     # Додаємо суму

    # Counter зручно підраховує кількість входжень кожного елемента
    sum_counts = Counter(sums)
    return sum_counts, num_simulations

def calculate_probabilities(sum_counts, num_simulations):
    """
    Обчислює ймовірності кожної суми на основі частот.

    Args:
        sum_counts (dict): Словник з частотами кожної суми.
        num_simulations (int): Загальна кількість симуляцій.

    Returns:
        dict: Словник, де ключ - сума, значення - її ймовірність.
    """
    probabilities = {}
    for s in range(2, 13): # Можливі суми від 2 до 12
        # Якщо сума не випадала жодного разу, її частота буде 0
        count = sum_counts.get(s, 0)
        probabilities[s] = count / num_simulations
    return probabilities

def plot_probabilities(mc_probabilities, analytical_probabilities):
    """
    Створює графік, який відображає ймовірності сум.

    Args:
        mc_probabilities (dict): Ймовірності, отримані методом Монте-Карло.
        analytical_probabilities (dict): Аналітично розраховані ймовірності.
    """
    sums = sorted(list(mc_probabilities.keys()))
    mc_values = [mc_probabilities[s] for s in sums]
    analytical_values = [analytical_probabilities[s] for s in sums]

    plt.figure(figsize=(10, 6))
    plt.bar([s - 0.2 for s in sums], mc_values, width=0.4, label='Монте-Карло', alpha=0.7, color = 'red')
    plt.bar([s + 0.2 for s in sums], analytical_values, width=0.4, label='Аналітичні', alpha=0.7, color = 'mediumseagreen')

    plt.xlabel('Сума чисел на кубиках')
    plt.ylabel('Ймовірність')
    plt.title('Порівняння ймовірностей сум кидків двох кубиків')
    plt.xticks(sums)
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

def get_analytical_probabilities():
    """
    Обчислює аналітичні (теоретичні) ймовірності сум кидків двох кубиків.
    """
    # Всього можливих комбінацій: 6 * 6 = 36
    total_outcomes = 36
    
    # Частоти для кожної суми
    # Сума 2: (1,1) - 1 комбінація
    # Сума 3: (1,2), (2,1) - 2 комбінації
    # Сума 4: (1,3), (2,2), (3,1) - 3 комбінації
    # Сума 5: (1,4), (2,3), (3,2), (4,1) - 4 комбінації
    # Сума 6: (1,5), (2,4), (3,3), (4,2), (5,1) - 5 комбінацій
    # Сума 7: (1,6), (2,5), (3,4), (4,3), (5,2), (6,1) - 6 комбінацій
    # Сума 8: (2,6), (3,5), (4,4), (5,3), (6,2) - 5 комбінацій
    # Сума 9: (3,6), (4,5), (5,4), (6,3) - 4 комбінації
    # Сума 10: (4,6), (5,5), (6,4) - 3 комбінації
    # Сума 11: (5,6), (6,5) - 2 комбінації
    # Сума 12: (6,6) - 1 комбінація
    
    analytical_counts = {
        2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6,
        8: 5, 9: 4, 10: 3, 11: 2, 12: 1
    }
    
    analytical_probs = {s: count / total_outcomes for s, count in analytical_counts.items()}
    return analytical_probs

if __name__ == "__main__":
    # Кількість симуляцій (можна змінювати для тестування)
    num_simulations = 1000000  # Один мільйон кидків для хорошої точності

    print(f"Починаємо симуляцію {num_simulations} кидків двох кубиків методом Монте-Карло...")

    # Крок 1 і 2: Імітація та підрахунок частот
    sum_counts, total_sims = monte_carlo_dice_roll(num_simulations)

    # Крок 3: Обчислення ймовірностей методом Монте-Карло
    mc_probabilities = calculate_probabilities(sum_counts, total_sims)

    # Обчислення аналітичних ймовірностей
    analytical_probabilities = get_analytical_probabilities()

    # Створення таблиці для відображення результатів
    results_df = pd.DataFrame({
        'Сума': sorted(mc_probabilities.keys()),
        'Монте-Карло Ймовірність': [mc_probabilities[s] for s in sorted(mc_probabilities.keys())],
        'Аналітична Ймовірність': [analytical_probabilities[s] for s in sorted(analytical_probabilities.keys())]
    })
    results_df = results_df.set_index('Сума')
    results_df['Відхилення (%)'] = ((results_df['Монте-Карло Ймовірність'] - results_df['Аналітична Ймовірність']) / results_df['Аналітична Ймовірність']).abs() * 100

    print("\nТаблиця ймовірностей:")
    print(results_df.to_string(float_format="%.4f")) # Виводимо до 4 знаків після коми

    # Крок 4: Створення графіка
    plot_probabilities(mc_probabilities, analytical_probabilities)

    print("\nСимуляція завершена. Графік відображено.")
    print("Будь ласка, перегляньте файл readme.md для висновків.")