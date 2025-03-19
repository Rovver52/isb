import argparse
from constant import ALPHABET


def create_polybius_square(key, alphabet):
    """Создает квадрат Полибия на основе ключа и алфавита.

    Args:
        key (str): Ключ шифрования.
        alphabet (str): Алфавит для шифрования.

    Returns:
        list: Квадрат Полибия (6x6).
    """
    key = "".join(dict.fromkeys(key))

    square = []
    used_chars = set()

    for char in key:
        if char in alphabet and char not in used_chars:
            square.append(char)
            used_chars.add(char)

    for char in alphabet:
        if char not in used_chars:
            square.append(char)

    polybius_square = [square[i:i + 6] for i in range(0, len(square), 6)]
    return polybius_square


def encrypt(text, polybius_square):
    """Шифрует текст с использованием квадрата Полибия.

    Args:
        text (str): Исходный текст для шифрования.
        polybius_square (list): Квадрат Полибия.

    Returns:
        str: Зашифрованный текст.
    """
    encrypted_text = ""
    for char in text.upper():
        if char in ALPHABET:
            for i in range(len(polybius_square)):
                if char in polybius_square[i]:
                    row = i + 1
                    col = polybius_square[i].index(char) + 1
                    encrypted_text += f"{row}{col}"
                    break
        else:
            encrypted_text += char
    return encrypted_text


def main():
    """Основная функция для обработки аргументов и выполнения шифрования."""
    parser = argparse.ArgumentParser(
        description="Шифрование текста методом квадрата Полибия."
    )
    parser.add_argument(
        "--key", type=str, required=True, help="Ключ шифрования"
    )
    parser.add_argument(
        "--text", type=str, help="Текст для шифрования"
    )
    parser.add_argument(
        "--input", "-i", type=str, help="Путь к файлу с исходным текстом"
    )
    parser.add_argument(
        "--output", "-o", type=str, help="Путь к файлу для сохранения зашифрованного текста"
    )
    args = parser.parse_args()

    if args.input:
        try:
            with open(args.input, "r", encoding="utf-8") as file:
                text = file.read()
        except Exception as e:
            print(f"Ошибка при чтении файла: {e}")
            return
    elif args.text:
        text = args.text
    else:
        print("Ошибка: Необходимо указать либо --text, либо --input.")
        return

    polybius_square = create_polybius_square(args.key.upper(), ALPHABET)

    encrypted_text = encrypt(text.upper(), polybius_square)

    print("Зашифрованный текст:", encrypted_text)

    if args.output:
        try:
            with open(args.output, "w", encoding="utf-8") as file:
                file.write(encrypted_text)
            print(f"Зашифрованный текст сохранен в файл: {args.output}")
        except Exception as e:
            print(f"Ошибка при сохранении файла: {e}")


if __name__ == "__main__":
    main()