import os

from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


class SymmetricCrypto:
    """Класс для работы с симметричным шифрованием (AES)"""

    @staticmethod
    def generate_key(key_size: int) -> bytes:
        """Генерирует симметричный ключ заданного размера"""
        if key_size not in [128, 192, 256]:
            raise ValueError("Неподдерживаемый размер ключа")
        return os.urandom(key_size // 8)

    @staticmethod
    def encrypt_data(data: bytes, key: bytes) -> bytes:
        """Шифрует данные симметричным ключом"""
        padder = padding.ANSIX923(128).padder()
        padded_data = padder.update(data) + padder.finalize()

        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        return iv + encryptor.update(padded_data) + encryptor.finalize()

    @staticmethod
    def decrypt_data(encrypted_data: bytes, key: bytes) -> bytes:
        """Дешифрует данные симметричным ключом"""
        iv = encrypted_data[:16]
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
        decryptor = cipher.decryptor()
        decrypted_padded = decryptor.update(encrypted_data[16:]) + decryptor.finalize()

        unpadder = padding.ANSIX923(128).unpadder()
        return unpadder.update(decrypted_padded) + unpadder.finalize()