"""Точка входа: запуск приложения ROT13 Cipher."""

from gui import RotApp


def main():
    app = RotApp()
    app.mainloop()


if __name__ == "__main__":
    main()