import os
import subprocess
import sys
import ctypes
import urllib.request
import shutil


def is_admin():
    """проверка, запущена ли программа с правами админа"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception as text:
        print(text)
        return False


def run_as_admin():
    """
    Перезапускает текущий скрипт с правами администратора

    Использует Windows API ShellExecuteW с параметром "runas" для запуска программы
    с повышенными правами доступа. После вызова этой функции текущий процесс завершается.

    """
    script = os.path.abspath(sys.argv[0])
    params = ' '.join([f'"{param}"' for param in sys.argv[1:]])
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{script}" {params}', None, 1)
    sys.exit(0)


def download_tesseract_installer(url, installer_path):
    """
    Скачивает установщик Tesseract по указанному URL
    :param url: Прямая ссылка на установочный файл
    :param installer_path: Локальный путь, куда сохранить установщик

    """
    print(f"установка Tesseract с {url}...")
    try:
        # Скачиваем установщик
        urllib.request.urlretrieve(url, installer_path)
        print("установщик Tesseract установлен.")
    except Exception as e:
        print(f"Ошибка установки Tesseract: {e}")
        quit()


def run_tesseract_installer(installer_path):
    """
    Запускает установщик Tesseract
    :param installer_path: Путь к скачанному установщику

    """
    print("Запускаем программу установки Tesseract...")
    try:
        subprocess.run([installer_path], check=True)
        print("Установка Tesseract завершена.")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при установке Tesseract: {e}")
        quit()


def begin_install_tesseract():
    """
    функция проверяет права администратора и при необходимости запрашивает их.

    tesseract_url - Ссылка на предварительно собранные бинарники Tesseract для Windows
    installer_path - путь к установщику
    """
    tesseract_url = ("https://github.com/tesseract-ocr/tesseract/releases/download/"
                     "5.5.0/tesseract-ocr-w64-setup-5.5.0.20241111.exe")
    installer_path = "tesseract-ocr-setup.exe"

    if not is_admin():
        print("Запрос прав администратора...")
        run_as_admin()

    download_tesseract_installer(tesseract_url, installer_path)
    run_tesseract_installer(installer_path)


if __name__ == "__main__":
    begin_install_tesseract()
