"""Логика шифрования: ROT13 для английского и аналог ROT13 для русского."""

LANGUAGE_ENGLISH = "English — ROT13"
LANGUAGE_RUSSIAN = "Русский — аналог ROT13"

SHIFT = 13

ENGLISH_UPPER = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# В русском алфавите 33 буквы. Ё стоит в КОНЦЕ (после Я).
# Из-за этого А -> Н, Б -> О, В -> П, ..., а Ё/ё обрабатывается как обычная буква.
RUSSIAN_UPPER = "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯЁ"

ALPHABETS = {
    LANGUAGE_ENGLISH: (ENGLISH_UPPER, ENGLISH_UPPER.lower()),
    LANGUAGE_RUSSIAN: (RUSSIAN_UPPER, RUSSIAN_UPPER.lower()),
}


def shift_text(text, upper_letters, lower_letters, shift):
    """Сдвигает буквы алфавита на shift позиций по кругу.

    Все остальные символы (цифры, пробелы, знаки препинания,
    буквы другого алфавита) остаются без изменений.
    """
    alphabet_size = len(upper_letters)
    result = []

    for character in text:
        if character in upper_letters:
            position = upper_letters.index(character)
            result.append(upper_letters[(position + shift) % alphabet_size])
        elif character in lower_letters:
            position = lower_letters.index(character)
            result.append(lower_letters[(position + shift) % alphabet_size])
        else:
            result.append(character)

    return "".join(result)


def encrypt(text, language):
    """Шифрует текст: сдвиг вперёд на 13 букв."""
    upper_letters, lower_letters = ALPHABETS[language]
    return shift_text(text, upper_letters, lower_letters, SHIFT)


def decrypt(text, language):
    """Расшифровывает текст.

    English: 26 букв, поэтому сдвиг +13 и -13 дают одинаковый результат
    (ROT13 симметричен) -- по сути, это та же операция, что и шифрование.
    Русский: 33 буквы, поэтому нужен сдвиг назад на 13 (-13).
    """
    upper_letters, lower_letters = ALPHABETS[language]
    return shift_text(text, upper_letters, lower_letters, -SHIFT)