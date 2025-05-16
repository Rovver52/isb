class FileManager:
    """Класс для работы с файлами"""

    @staticmethod
    def save_file(path: str, data: bytes) -> None:
        """Сохраняет данные в файл"""
        with open(path, 'wb') as f:
            f.write(data)

    @staticmethod
    def load_file(path: str) -> bytes:
        """Загружает данные из файла"""
        with open(path, 'rb') as f:
            return f.read()

    @staticmethod
    def read_text_file(path: str) -> str:
        """Читает текстовый файл"""
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()

    @staticmethod
    def write_text_file(path: str, text: str) -> None:
        """Записывает текст в файл"""
        with open(path, 'w', encoding='utf-8') as f:
            f.write(text)