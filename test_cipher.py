"""Тесты для cipher.py. Запуск: python -m unittest test_cipher -v"""

import unittest

import cipher

EN = cipher.LANGUAGE_ENGLISH
RU = cipher.LANGUAGE_RUSSIAN


class EnglishRot13Tests(unittest.TestCase):
    def test_hello_world(self):
        self.assertEqual(cipher.encrypt("Hello World", EN), "Uryyb Jbeyq")

    def test_decrypt(self):
        self.assertEqual(cipher.decrypt("Uryyb Jbeyq", EN), "Hello World")

    def test_symmetry(self):
        self.assertEqual(cipher.encrypt(cipher.encrypt("Python", EN), EN), "Python")

    def test_edges(self):
        self.assertEqual(cipher.encrypt("AMNZ amnz", EN), "NZAM nzam")


class RussianAnalogTests(unittest.TestCase):
    def test_start_of_alphabet(self):
        self.assertEqual(cipher.encrypt("АБВ абв", RU), "НОП ноп")

    def test_privet(self):
        self.assertEqual(cipher.encrypt("ПРИВЕТ", RU), "ЬЭХПТЯ")
        self.assertEqual(cipher.decrypt("ЬЭХПТЯ", RU), "ПРИВЕТ")

    def test_moskva_case(self):
        self.assertEqual(cipher.encrypt("Москва", RU), "Щыючпн")

    def test_yo(self):
        self.assertEqual(cipher.encrypt("Ёж", RU), "Му")
        self.assertEqual(cipher.decrypt("Му", RU), "Ёж")

    def test_wrap_around(self):
        self.assertEqual(cipher.encrypt("Яблоко", RU), "Лошычы")

    def test_round_trip_all_letters(self):
        text = "Съешь ещё этих мягких французских булок, да выпей чаю!"
        self.assertEqual(cipher.decrypt(cipher.encrypt(text, RU), RU), text)

    def test_russian_is_not_symmetric(self):
        self.assertNotEqual(cipher.encrypt(cipher.encrypt("Привет", RU), RU), "Привет")


class PreservationTests(unittest.TestCase):
    def test_digits_and_punctuation_unchanged(self):
        text = '123 .,;:!? ()[]{} "кавычки" \'abc\' - _ @#'
        self.assertEqual(cipher.encrypt("123 .,!?()", EN), "123 .,!?()")
        self.assertEqual(cipher.encrypt("123 .,!?()", RU), "123 .,!?()")
        self.assertEqual(cipher.decrypt(cipher.encrypt(text, RU), RU), text)

    def test_mixed_text(self):
        self.assertEqual(cipher.encrypt("Hello, Привет! 123", EN), "Uryyb, Привет! 123")
        self.assertEqual(cipher.encrypt("Hello, Привет! 123", RU), "Hello, Ьэхптя! 123")


if __name__ == "__main__":
    unittest.main()