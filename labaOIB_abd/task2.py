import json
from constant2 import RUSSIAN_LETTER_FREQ, RUS_FREQ, COD1_Z, CIPH, KEY, DECRYPTED_DATA


def save_dict_to_json(file_path: str, data: dict) -> None:
    """
    Сохраняет словарь в JSON-файл.
    :param file_path: Путь к файлу.
    :param data: Словарь для сохранения.
    """
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def load_dict_from_json(file_path: str) -> dict:
    """
    Загружает словарь из JSON-файла.
    :param file_path: Путь к файлу.
    :return: Загруженный словарь.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def compute_char_frequencies(input_text: str) -> dict:
    """
    Вычисляет частоту появления каждого символа в тексте.
    :param input_text: Текст для анализа.
    :return: Словарь с частотами символов.
    """
    char_count = {}
    for char in input_text:
        if char in char_count:
            char_count[char] += 1
        else:
            char_count[char] = 1

    total_chars = sum(char_count.values())
    char_freq = {char: round(count / total_chars, 6) for char, count in char_count.items()}

    sorted_freq = dict(sorted(char_freq.items(), key=lambda item: item[1], reverse=True))
    return sorted_freq

def generate_char_mapping(cipher_freq: dict, lang_freq: dict) -> dict:
    """
    Создает сопоставление между символами зашифрованного текста и символами языка.
    :param cipher_freq: Частоты символов зашифрованного текста.
    :param lang_freq: Частоты символов языка.
    :return: Словарь сопоставления.
    """
    cipher_chars = list(cipher_freq.keys())
    lang_chars = list(lang_freq.keys())

    mapping = {}
    for i in range(min(len(cipher_chars), len(lang_chars))):
        mapping[cipher_chars[i]] = lang_chars[i]
    return mapping

def apply_char_mapping(encrypted_text: str, mapping: dict) -> str:
    """
    Применяет сопоставление символов для расшифровки текста.
    :param encrypted_text: Зашифрованный текст.
    :param mapping: Словарь сопоставления символов.
    :return: Расшифрованный текст.
    """
    decrypted_text = []
    for char in encrypted_text:
        decrypted_text.append(mapping.get(char, char))
    return ''.join(decrypted_text)

def write_text_to_file(file_path: str, text: str) -> None:
    """
    Записывает текст в файл.
    :param file_path: Путь к файлу.
    :param text: Текст для записи.
    """
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(text)

def read_text_from_file(file_path: str) -> str:
    """
    Читает текст из файла.
    :param file_path: Путь к файлу.
    :return: Прочитанный текст.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def main():
    save_dict_to_json(RUS_FREQ, RUSSIAN_LETTER_FREQ)

    encrypted_text = read_text_from_file(COD1_Z)

    text_freq = compute_char_frequencies(encrypted_text)
    save_dict_to_json(CIPH, text_freq)


    key_mapping = load_dict_from_json(KEY)

    decrypted_text = apply_char_mapping(encrypted_text, key_mapping)

    write_text_to_file(DECRYPTED_DATA, decrypted_text)

if __name__ == '__main__':
    main()