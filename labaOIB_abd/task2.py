import json

from constant2 import (
    RUSSIAN_LETTER_FREQ,
    RUS_FREQ,
    COD1_Z,
    CIPH,
    KEY,
    DECRYPTED_DATA,
)


def save_dict_to_json(file_path: str, data: dict) -> None:
    """Сохраняет словарь в JSON-файл.

    Args:
        file_path (str): Путь к файлу.
        data (dict): Словарь для сохранения.
    """
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
    except IOError as e:
        print(f"Ошибка при записи в файл {file_path}: {e}")
    except TypeError as e:
        print(f"Ошибка сериализации данных в JSON: {e}")


def load_dict_from_json(file_path: str) -> dict:
    """Загружает словарь из JSON-файла.

    Args:
        file_path (str): Путь к файлу.

    Returns:
        dict: Загруженный словарь.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except IOError as e:
        print(f"Ошибка при чтении файла {file_path}: {e}")
        return {}
    except json.JSONDecodeError as e:
        print(f"Ошибка декодирования JSON из файла {file_path}: {e}")
        return {}


def compute_char_frequencies(input_text: str) -> dict:
    """Вычисляет частоту появления каждого символа в тексте.

    Args:
        input_text (str): Текст для анализа.

    Returns:
        dict: Словарь с частотами символов.
    """
    char_count = {}
    for char in input_text:
        if char in char_count:
            char_count[char] += 1
        else:
            char_count[char] = 1

    total_chars = sum(char_count.values())
    char_freq = {
        char: round(count / total_chars, 6) for char, count in char_count.items()
    }

    sorted_freq = dict(sorted(char_freq.items(), key=lambda item: item[1], reverse=True))
    return sorted_freq


def generate_char_mapping(cipher_freq: dict, lang_freq: dict) -> dict:
    """Создает сопоставление между символами зашифрованного текста и символами языка.

    Args:
        cipher_freq (dict): Частоты символов зашифрованного текста.
        lang_freq (dict): Частоты символов языка.

    Returns:
        dict: Словарь сопоставления.
    """
    cipher_chars = list(cipher_freq.keys())
    lang_chars = list(lang_freq.keys())

    mapping = {}
    for i in range(min(len(cipher_chars), len(lang_chars))):
        mapping[cipher_chars[i]] = lang_chars[i]
    return mapping


def apply_char_mapping(encrypted_text: str, mapping: dict) -> str:
    """Применяет сопоставление символов для расшифровки текста.

    Args:
        encrypted_text (str): Зашифрованный текст.
        mapping (dict): Словарь сопоставления символов.

    Returns:
        str: Расшифрованный текст.
    """
    decrypted_text = []
    for char in encrypted_text:
        decrypted_text.append(mapping.get(char, char))
    return "".join(decrypted_text)


def write_text_to_file(file_path: str, text: str) -> None:
    """Записывает текст в файл.

    Args:
        file_path (str): Путь к файлу.
        text (str): Текст для записи.
    """
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(text)
    except IOError as e:
        print(f"Ошибка при записи в файл {file_path}: {e}")


def read_text_from_file(file_path: str) -> str:
    """Читает текст из файла.

    Args:
        file_path (str): Путь к файлу.

    Returns:
        str: Прочитанный текст.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except IOError as e:
        print(f"Ошибка при чтении файла {file_path}: {e}")
        return ""


def main():
    """Основная функция для выполнения шифрования и расшифровки."""
    save_dict_to_json(RUS_FREQ, RUSSIAN_LETTER_FREQ)

    encrypted_text = read_text_from_file(COD1_Z)
    if not encrypted_text:
        print("Не удалось прочитать зашифрованный текст.")
        return

    text_freq = compute_char_frequencies(encrypted_text)
    save_dict_to_json(CIPH, text_freq)

    key_mapping = load_dict_from_json(KEY)
    if not key_mapping:
        print("Не удалось загрузить сопоставление ключей.")
        return

    decrypted_text = apply_char_mapping(encrypted_text, key_mapping)

    write_text_to_file(DECRYPTED_DATA, decrypted_text)


if __name__ == "__main__":
    main()