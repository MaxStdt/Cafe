"""
Задача "Кафе" — жадный алгоритм с динамическим ранжированием.

Идея:
  Строим список дней, отсортированный по убыванию цены (Структура1).
  Идём по дням слева направо. Для текущего дня находим его ранг
  среди ЕЩЁ НЕ ОБРАБОТАННЫХ дней. Если накопленных купонов >= ранга,
  тратим купон (день бесплатный), иначе платим; при цене > 100
  получаем купон. После обработки удаляем день из Структуры1.

  Правило "coupons >= rank" означает "купонов строго больше, чем
  будущих более дорогих дней" -> трата купона на текущий (более
  дешёвый) день безопасна: купонов всё равно хватит на все более
  дорогие будущие дни.

Ввод/вывод — через файлы input.txt / output.txt.
"""

import sys

COUPON_THRESHOLD = 100  # строго больше этой суммы — купон


def solve(n, costs):
    """
    Жадное решение задачи.

    Параметры:
        n     : количество дней
        costs : список цен (0-based, length = n)

    Возвращает:
        total     : минимальная суммарная стоимость
        k1        : число неиспользованных купонов в конце
        k2        : число использованных купонов
        free_days : список номеров дней, оплаченных купоном,
                    в возрастающем порядке
    """
    # --- Шаг 1: строим Структуру1 ---
    # Каждый элемент: (цена, номер_дня_1based).
    # Сортировка: по цене по убыванию; при равенстве — по номеру дня
    # по возрастанию (детерминированность).
    structure = [(costs[i], i + 1) for i in range(n)]
    structure.sort(key=lambda x: (-x[0], x[1]))

    # --- Шаг 2: проход по дням слева направо ---
    coupons = 0        # накопленные неиспользованные купоны
    total = 0          # суммарные затраты
    free_days = []     # дни, оплаченные купоном (1-based)

    for i in range(n):
        day_num = i + 1
        price = costs[i]

        # Находим текущий ранг дня day_num в Структуре1.
        # Ранг = позиция в списке + 1 (1 = самый дорогой среди оставшихся).
        rank = 0
        for idx, (p, d) in enumerate(structure):
            if d == day_num:
                rank = idx + 1
                break

        # rank всегда найдётся: день ещё не удалён (мы его обрабатываем сейчас)
        # --- Решение: тратим купон или платим ---
        if coupons >= rank:
            # Купонов строго больше, чем будущих более дорогих дней:
            # тратим купон на текущий день.
            coupons -= 1
            free_days.append(day_num)
            # total += 0
        else:
            # Платим за день.
            total += price
            if price > COUPON_THRESHOLD:
                coupons += 1  # получили купон

        # --- Шаг 3: удаляем обработанный день из Структуры1 ---
        # (независимо от того, заплатили или потратили купон)
        # Находим индекс и удаляем. Для простоты — через list comprehension
        # или del по индексу. Здесь del по найденному индексу.
        for idx, (p, d) in enumerate(structure):
            if d == day_num:
                del structure[idx]
                break

    k2 = len(free_days)
    k1 = coupons

    return total, k1, k2, free_days


def main():
    # --- Определение путей входного и выходного файлов ---
    # Если переданы аргументы командной строки — используем их:
    #   python main.py <input_file> <output_file>
    # Иначе — значения по умолчанию: input.txt и output.txt
    input_path = sys.argv[1] if len(sys.argv) > 1 else "input.txt"
    output_path = sys.argv[2] if len(sys.argv) > 2 else "output.txt"

    # --- Чтение входных данных ---
    try:
        with open(input_path, "r", encoding="utf-8") as f:
            data = f.read().split()
    except FileNotFoundError:
        print(f"Ошибка: файл {input_path} не найден.", file=sys.stderr)
        return 1

    if not data:
        print(f"Ошибка: пустой входной файл {input_path}.", file=sys.stderr)
        return 1

    n = int(data[0])
    if n <= 0:
        print("Ошибка: N должно быть положительным.", file=sys.stderr)
        return 1

    costs = [int(x) for x in data[1:1 + n]]
    if len(costs) != n:
        print("Ошибка: недостаточно данных о стоимостях.", file=sys.stderr)
        return 1

    # --- Решение ---
    total, k1, k2, free_days = solve(n, costs)

    # --- Запись выходных данных ---
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(f"{total}\n")
            f.write(f"{k1} {k2}\n")
            for d in free_days:
                f.write(f"{d}\n")
    except OSError as e:
        print(f"Ошибка записи в файл {output_path}: {e}", file=sys.stderr)
        return 1

    # --- Сообщение об успешности (стандартный поток) ---
    print("Программа успешно выполнена.")
    print(f"Входной файл: {input_path}")
    print(f"Выходной файл: {output_path}")
    print(f"Минимальная сумма: {total}")
    print(f"K1 (неиспользованных купонов): {k1}")
    print(f"K2 (использованных купонов): {k2}")
    if free_days:
        print(f"Дни с купонами: {free_days}")
    else:
        print("Дни с купонами: (нет)")

    return 0


if __name__ == "__main__":
    sys.exit(main())