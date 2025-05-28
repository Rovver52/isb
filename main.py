import json

from func_run import CardFinder, run_experiment


def main():
    finder = CardFinder()

    while True:
        print("\nМеню:")
        print("1: Подбор номера карты")
        print("2: Проверка корректности номера")
        print("3: Замер времени для поиска коллизии хеша при различном числе процессов")
        print("4: Выход")

        choice = input("Выберите пункт меню: ")

        if choice == "1":
            # Подбор номера карты
            print("\nПодбор номера карты...")
            result = None
            for bin in finder.bins:
                result = finder.find_card_number(bin)
                if result:
                    break

            if result:
                print(f"Найден номер карты: {result}")
                report = finder.get_report(result, bin)
                finder.write_report(report)
                print(f"Отчет сохранен в {finder.json_res}")
            else:
                print("Номер карты не найден")
                report = finder.get_report(None, finder.bins[0])
                finder.write_report(report)


        elif choice == "2":

            # Проверка корректности номера

            print("\nПроверка корректности номера карты...")

            # Проверяем, есть ли сохраненная карта в файле

            try:

                with open(finder.json_res, 'r') as file:

                    data = json.load(file)

                    if 'card_number' in data and data['card_number']:

                        card_number = data['card_number']

                        print(f"Найдена сохраненная карта: {card_number}")

                        if finder.luhn_check(card_number):

                            print("Номер карты корректен (прошел проверку Луна)")

                        else:

                            print("Номер карты некорректен (не прошел проверку Луна)")

                    else:

                        print("В файле результатов нет сохраненного номера карты")

                        card_number = input("Введите номер карты для проверки вручную: ")

                        if finder.luhn_check(card_number):

                            print("Номер карты корректен (прошел проверку Луна)")

                        else:

                            print("Номер карты некорректен (не прошел проверку Луна)")

            except FileNotFoundError:

                print("Файл с результатами не найден, введите номер карты вручную")

                card_number = input("Введите номер карты для проверки: ")

                if finder.luhn_check(card_number):

                    print("Номер карты корректен (прошел проверку Луна)")

                else:

                    print("Номер карты некорректен (не прошел проверку Луна)")

            except json.JSONDecodeError:

                print("Ошибка чтения файла результатов, введите номер карты вручную")

                card_number = input("Введите номер карты для проверки: ")

                if finder.luhn_check(card_number):

                    print("Номер карты корректен (прошел проверку Луна)")

                else:

                    print("Номер карты некорректен (не прошел проверку Луна)")

        elif choice == "3":
            result_file = "../isb/card_search_result.json"
            run_experiment(result_file)
            print("График сохранен в файл time_graph.png")

        elif choice == "4":
            # Выход
            print("Выход из программы")
            break

        else:
            print("Неверный выбор. Пожалуйста, выберите пункт от 1 до 4")


if __name__ == "__main__":
    main()