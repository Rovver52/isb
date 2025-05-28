import json
import multiprocessing
import time
import hashlib
import itertools
import constants

import matplotlib.pyplot as plt

from typing import Generator


class CardFinder:
    def __init__(self):
        self.bins = constants.SBERBANK_VISA_DEBIT_BINS
        self.hash = constants.HASH
        self.last_four = constants.LAST_FOUR
        self.json_res = constants.JSON_RES

    def generate_possible_numbers(self, bin: str) -> Generator[str, None, None]:
        middle_length = 6
        for middle in itertools.product('0123456789', repeat=middle_length):
            yield bin + ''.join(middle) + self.last_four

    @staticmethod
    def check_card_hash(args: tuple[str, str]) -> str | None:
        hash, card_number = args
        hashed = hashlib.blake2b(card_number.encode(), digest_size=64).hexdigest()
        return card_number if hash == hashed else None

    @staticmethod
    def get_num_processes() -> int:
        return multiprocessing.cpu_count()

    def find_card_number(self, bin: str, num_processes=get_num_processes()) -> str | None:
        result = None
        with multiprocessing.Pool(processes=num_processes) as pool:
            tasks = ((self.hash, num) for num in self.generate_possible_numbers(bin))  # создание генератора задач
            for res in pool.imap_unordered(self.check_card_hash, tasks):
                if res:
                    result = res
                    break
        return result

    def get_graph(self, time_data: list) -> None:
        processes = list(range(1, int(self.get_num_processes() * 1.5) + 1))
        plt.figure(figsize=(10, 5))
        plt.plot(processes, time_data)

        plt.title("Time dependence on the number of processes")
        plt.xlabel("Number of processes")
        plt.ylabel("Time (seconds)")

        plt.xticks(processes)
        plt.grid(True)

        min_time = min(time_data)
        min_processes = time_data.index(min_time) + 1
        plt.scatter(min_processes, min_time, color="red", label="Point of global minimum")
        plt.savefig("time_graph.png")  # Сохраняем график в файл
        plt.close()

    def get_report(self, result: str | None, bin: str) -> dict[str, str | None | int]:
        report = {
            "status": "success" if result else "fail",
            "card_number": result,
            "bin": bin,
            "last_four_numbers": self.last_four,
            "hash": self.hash,
            "processes_used": self.get_num_processes()
        }
        return report

    def write_report(self, report: dict[str, str | None | int]) -> None:
        with open(self.json_res, 'w') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

    @staticmethod
    def luhn_check(card_number: str) -> bool:
        numbers = [int(d) for d in reversed(card_number)]

        for i in range(1, len(card_number), 2):
            doubled = numbers[i] * 2
            numbers[i] = doubled - 9 if doubled > 9 else doubled

        return sum(numbers) % 10 == 0

    def get_json_data(self):
        with open(self.json_res, 'r') as file:
            data = json.load(file)
        return data

    def clear_report(self):
        with open(self.json_res, 'w') as file:
            json.dump({}, file)


def run_experiment(result_file: str = "card.search_result.json"):
    """Замер времени для поиска коллизии хеша при различном числе процессов"""

    # Загружаем данные из файла с результатами поиска
    try:
        with open(result_file, 'r') as f:
            search_result = json.load(f)
    except FileNotFoundError:
        print(f"Ошибка: файл {result_file} не найден")
        return
    except json.JSONDecodeError:
        print(f"Ошибка: файл {result_file} содержит некорректный JSON")
        return

    # Проверяем необходимые поля в данных
    required_fields = ['hash', 'last_four_numbers', 'bin']
    for field in required_fields:
        if field not in search_result:
            print(f"Ошибка: в файле отсутствует обязательное поле {field}")
            return

    # Создаем временный экземпляр CardFinder с настройками из файла
    finder = CardFinder()
    finder.hash = search_result['hash']
    finder.last_four = search_result['last_four_numbers']
    finder.bins = [search_result['bin']]  # Используем только тот BIN, который был в результатах

    num_processes = int(finder.get_num_processes() * 1.5)
    time_res = []

    print(f"\nЗамер времени для поиска коллизии хеша...")
    print(f"Используются параметры из файла {result_file}:")
    print(f"BIN: {search_result['bin']}")
    print(f"Последние 4 цифры: {search_result['last_four_numbers']}")
    print(f"Хеш: {search_result['hash'][:16]}...")

    for i in range(1, num_processes + 1):
        time_start = time.time()
        # Ищем только для одного BIN, который был в результатах
        if finder.find_card_number(search_result['bin'], i):
            res = time.time() - time_start
            time_res.append(res)

    if not time_res:
        print("Не удалось найти коллизию хеша для замера времени")
        return

    finder.get_graph(time_res)
    print("График сохранен в файл time_graph.png")