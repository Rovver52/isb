import math

from typing import Tuple, List
from scipy.special import gammainc

from constant import P


def bit_frequency_analysis(sequence: str) -> float:
    """
    Выполняет анализ частоты битов в бинарной последовательности.

    Args:
        sequence: Строка из '0' и '1' для анализа.

    Returns:
        P_value: P-значение теста частот.
    """
    sum_seq = 0
    length = len(sequence)
    for i in sequence:
        match i:
            case '1':
                sum_seq += 1
            case '0':
                sum_seq += -1

    Sn = (1 / (length ** 0.5)) * sum_seq
    P_value = math.erfc(Sn / (2 ** 0.5))
    return P_value


def identical_consecutive_bits(sequence: str) -> float:
    """
    Проверяет последовательность на идентичные подряд идущие биты.

    Args:
        sequence: Строка из '0' и '1' для анализа.

    Returns:
        P_value: P-значение теста, или 0 если условия не выполнены.
    """
    length = len(sequence)
    count_1 = (1 / length) * sequence.count('1')
    if abs(count_1 - 0.5) < 2 / (length ** 0.5):
        Vn = 0
        for i in range(length - 1):
            if sequence[i] != sequence[i + 1]:
                Vn += 1
        top = abs(Vn - 2 * length * count_1 * (1 - count_1))
        bot = 2 * ((2 * length) ** 0.5) * count_1 * (1 - count_1)
        P_value = math.erfc(top / bot)
        return P_value
    else:
        return 0


def split_sequence(sequence: str) -> List[str]:
    """
    Разбивает последовательность на блоки по 8 бит.

    Args:
        sequence: Строка из '0' и '1' длиной 128 бит.

    Returns:
        blocks: Список блоков по 8 бит.
    """
    length = len(sequence)
    blocks = [sequence[i:i + 8] for i in range(0, length, 8)]
    return blocks


def process_blocks(block: str) -> int:
    """
    Находит максимальную длину последовательности '1' в блоке.

    Args:
        block: Блок из 8 бит ('0' и '1').

    Returns:
        max_len: Максимальное количество подряд идущих '1'.
    """
    max_len = 0
    current_len = 0
    for bit in block:
        if bit == '1':
            current_len += 1
            max_len = max(current_len, max_len)
        else:
            current_len = 0
    return max_len


def distribution_into_groups(sequence: str) -> Tuple[int, int, int, int]:
    """
    Распределяет блоки по группам в зависимости от максимальной длины '1'.

    Args:
        sequence: Строка из '0' и '1' длиной 128 бит.

    Returns:
        Кортеж с количеством блоков в каждой группе (V1, V2, V3, V4).
    """
    V1, V2, V3, V4 = 0, 0, 0, 0
    blocks = split_sequence(sequence)
    for block in blocks:
        max_len = process_blocks(block)
        match max_len:
            case 1:
                V1 += 1
            case 2:
                V2 += 1
            case 3:
                V3 += 1
            case _:
                V4 += 1
    return V1, V2, V3, V4


def last_dance(groups: Tuple[int, int, int, int]) -> float:
    """
    Вычисляет итоговое P-значение на основе распределения по группам.

    Args:
        groups: Кортеж с количеством блоков в каждой группе.

    Returns:
        P-значение теста распределения.
    """
    X2 = 0
    for i in range(0, 4):
        X2 += ((groups[i] - 16 * P[i]) ** 2) / (16 * P[i])
    return gammainc(1.5, X2 / 2)