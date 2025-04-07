import argparse

import nist


def parse_arguments():
    """Парсинг аргументов командной строки"""
    parser = argparse.ArgumentParser(description="Анализатор случайных последовательностей")
    parser.add_argument("cpp_file", help="Путь к файлу с последовательностью C++")
    parser.add_argument("java_file", help="Путь к файлу с последовательностью Java")
    parser.add_argument("output_file", help="Файл для сохранения результатов")
    return parser.parse_args()


def open_file(filename: str) -> str:
    """Чтение последовательности из файла"""
    with open(filename, "r") as file:
        sequence = file.read()
    return sequence.strip()


def save_results(cpp_freq, java_freq,
                 cpp_cons, java_cons,
                 cpp_long, java_long,
                 output_file: str):
    """Сохранение результатов в файл"""
    with open(output_file, 'w') as f:
        f.write("Frequency bitwise test:\n")
        f.write(f"cpp: {cpp_freq}\n")
        f.write(f"java: {java_freq}\n\n")

        f.write("The consecutive identical bits test:\n")
        f.write(f"cpp: {cpp_cons}\n")
        f.write(f"java: {java_cons}\n\n")

        f.write("The longest sequence of units in block test:\n")
        f.write(f"cpp: {cpp_long}\n")
        f.write(f"java: {java_long}\n")


def main():
    args = parse_arguments()

    try:
        # Загрузка последовательностей
        cpp_seq = open_file(args.cpp_file)
        java_seq = open_file(args.java_file)

        # Проверка длины последовательностей
        if len(cpp_seq) != 128 or len(java_seq) != 128:
            raise ValueError("Последовательности должны быть длиной 128 бит")

        # Выполнение тестов
        cpp_freq = nist.bit_frequency_analysis(cpp_seq)
        java_freq = nist.bit_frequency_analysis(java_seq)

        cpp_cons = nist.identical_consecutive_bits(cpp_seq)
        java_cons = nist.identical_consecutive_bits(java_seq)

        cpp_long = nist.last_dance(nist.distribution_into_groups(cpp_seq))
        java_long = nist.last_dance(nist.distribution_into_groups(java_seq))

        # Сохранение результатов
        save_results(cpp_freq, java_freq,
                     cpp_cons, java_cons,
                     cpp_long, java_long,
                     args.output_file)

        print(f"Результаты успешно сохранены в {args.output_file}")

    except FileNotFoundError as e:
        print(f"Ошибка: файл не найден - {e}")
    except ValueError as e:
        print(f"Ошибка: {e}")
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")


if __name__ == "__main__":
    main()