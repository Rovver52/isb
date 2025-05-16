from typing import Optional
from dataclasses import dataclass
import json
import os
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from FileManager import FileManager
from AsymmetricCrypto import AsymmetricCrypto


@dataclass
class Config:
    """Конфигурация с путями к файлам"""
    PATHS: dict
    AES_KEY_SIZE: int = 256

    @classmethod
    def from_json(cls, config_path: str) -> 'Config':
        """Создает конфиг из JSON файла"""
        with open(config_path) as f:
            return cls(json.load(f))


class HybridCryptoSystem:
    """Гибридная криптосистема (RSA + AES)"""
    
    def __init__(self, config: Config):
        self.config = config
        self.asymmetric = AsymmetricCrypto()
        self.files = FileManager()

    def generate_and_save_keys(self, key_size: int = 256) -> None:
        """Генерирует и сохраняет ключи"""
        private_key, public_key = self.asymmetric.generate_keys()
        symmetric_key = os.urandom(key_size // 8)

        self.files.save_key(public_key, self.config.PATHS['PUBLIC_KEY'])
        self.files.save_key(private_key, self.config.PATHS['SECRET_KEY'])

        encrypted_sym_key = self.asymmetric.encrypt_with_public_key(
            public_key, symmetric_key
        )
        self.files.save_file(self.config.PATHS['SYMMETRIC_KEY'], encrypted_sym_key)

    def encrypt_file(
        self, 
        input_file: Optional[str] = None, 
        output_file: Optional[str] = None
    ) -> None:
        """Шифрует файл"""
        input_path = input_file or self.config.PATHS['INITIAL_FILE']
        output_path = output_file or self.config.PATHS['ENCRYPTED_FILE']

        private_key = self.files.load_private_key(self.config.PATHS['SECRET_KEY'])
        encrypted_sym_key = self.files.load_file(self.config.PATHS['SYMMETRIC_KEY'])
        symmetric_key = self.asymmetric.decrypt_with_private_key(
            private_key, encrypted_sym_key
        )

        data = self.files.load_file(input_path)
        padder = padding.ANSIX923(128).padder()
        padded_data = padder.update(data) + padder.finalize()

        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(symmetric_key), modes.CBC(iv))
        encrypted_data = iv + cipher.encryptor().update(padded_data) + cipher.encryptor().finalize()

        self.files.save_file(output_path, encrypted_data)

    def decrypt_file(
        self, 
        input_file: Optional[str] = None, 
        output_file: Optional[str] = None
    ) -> None:
        """Дешифрует файл"""
        input_path = input_file or self.config.PATHS['ENCRYPTED_FILE']
        output_path = output_file or self.config.PATHS['DECRYPTED_FILE']

        private_key = self.files.load_private_key(self.config.PATHS['SECRET_KEY'])
        encrypted_sym_key = self.files.load_file(self.config.PATHS['SYMMETRIC_KEY'])
        symmetric_key = self.asymmetric.decrypt_with_private_key(
            private_key, encrypted_sym_key
        )

        encrypted_data = self.files.load_file(input_path)
        iv = encrypted_data[:16]
        cipher = Cipher(algorithms.AES(symmetric_key), modes.CBC(iv))
        decrypted_padded = cipher.decryptor().update(encrypted_data[16:]) + cipher.decryptor().finalize()

        unpadder = padding.ANSIX923(128).unpadder()
        decrypted_data = unpadder.update(decrypted_padded) + unpadder.finalize()

        self.files.save_file(output_path, decrypted_data)
