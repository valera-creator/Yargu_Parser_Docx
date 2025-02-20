import subprocess
import ctypes
import urllib.request
import winreg
import os


def is_admin():
    """проверка, запущена ли программа с правами админа"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception as text:
        print(text)
        return False


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


def get_tesseract_installation_path():
    """
    Определяет путь установки Tesseract через реестр Windows.
    Вернет путь или None, если не удалось найти
    """
    try:
        # Открываем раздел реестра, где хранится информация о Tesseract
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Tesseract-OCR")
        # Получаем значение пути установки
        install_path, _ = winreg.QueryValueEx(key, "InstallDir")
        winreg.CloseKey(key)
        return install_path
    except FileNotFoundError:
        print("Не удалось найти путь установки Tesseract в реестре.")
        return None
    except Exception as e:
        print(f"Ошибка при чтении реестра: {e}")
        return None


def add_to_system_path(new_path):
    """
    Добавляет указанный путь в системную переменную окружения PATH в Windows.

    Логика работы:
        1. Проверяет права доступа: функция должна выполняться с правами администратора.
        2. Открывает раздел реестра Windows, где хранится значение переменной PATH
           (HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Environment).
        3. Читает текущее значение переменной PATH и проверяет его тип (должен быть REG_EXPAND_SZ).
        4. Проверяет, содержит ли текущее значение переменной PATH указанный путь (new_path).
        5. Если путь отсутствует, он добавляется в конец строки PATH, разделённый точкой с запятой (;).
        6. Обновлённое значение записывается обратно в реестр.
        7. В случае ошибок (например, недостаточно прав или неверный тип данных), выводится соответствующее сообщение.
    """

    try:
        # Открываем ключ реестра для записи
        with winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE) as hive:
            with winreg.OpenKey(hive, r'SYSTEM\CurrentControlSet\Control\Session Manager\Environment', 0,
                                winreg.KEY_SET_VALUE | winreg.KEY_QUERY_VALUE) as key:
                try:
                    # Читаем текущее значение PATH
                    current_path, reg_type = winreg.QueryValueEx(key, 'Path')

                    # Проверяем тип данных переменной PATH
                    if reg_type != winreg.REG_EXPAND_SZ:
                        print("Ошибка: Переменная PATH имеет неправильный тип данных.")
                        return

                    # Преобразуем в список
                    path_list = current_path.split(';') if current_path else []

                    # Проверяем, что новый путь еще не добавлен
                    if new_path not in path_list:
                        path_list.append(new_path)
                        updated_path = ';'.join(path_list)

                        # Записываем обновленное значение
                        winreg.SetValueEx(key, 'Path', 0, winreg.REG_EXPAND_SZ, updated_path)
                        print(f'Путь "{new_path}" успешно добавлен в системную переменную PATH.')
                    else:
                        print(f'Путь "{new_path}" уже существует в системной переменной PATH.')

                except FileNotFoundError:
                    # Если переменная PATH отсутствует, создаем её
                    winreg.SetValueEx(key, 'Path', 0, winreg.REG_EXPAND_SZ, new_path)
                    print(f'Переменная PATH создана, и путь "{new_path}" добавлен.')
                except PermissionError as text:
                    print(f"Ошибка доступа: {text}")
                except Exception as e:
                    print(f"Произошла ошибка при работе с реестром: {e}")

    except FileNotFoundError:
        print("Ошибка: Не удалось найти указанный раздел реестра.")
    except PermissionError as e:
        print(f"Ошибка: {e}")
    except Exception as e:
        print(f"Произошла общая ошибка: {e}")


def begin_install_tesseract():
    """
    функция проверяет права администратора и при необходимости запрашивает их.

    tesseract_url - Ссылка на предварительно собранные бинарники Tesseract для Windows
    installer_path - путь к установщику
    path_install - путь, где находится только что установленный Tesseract
    """

    tesseract_url = ("https://github.com/tesseract-ocr/tesseract/releases/download/"
                     "5.5.0/tesseract-ocr-w64-setup-5.5.0.20241111.exe")
    installer_path = "tesseract-ocr-setup.exe"

    if not is_admin():
        quit("Запустите программу от имени администратора")

    download_tesseract_installer(tesseract_url, installer_path)
    run_tesseract_installer(installer_path)
    path_install = get_tesseract_installation_path()

    if not path_install:
        print('Произошла ошибка при автоматическом определении пути установки Tesseract.')
        print('Внесите изменение переменных среды PATH самостоятельно.')
        return

    print(path_install)
    add_to_system_path(path_install)

    # удаляем exe
    os.remove(installer_path)

    # перезагружаем устройство, чтобы переменные среды зафиксировалась везде
    print('Перезагрузка устройства через 3 секунды:')
    os.system("shutdown /r /t 3")


if __name__ == "__main__":
    begin_install_tesseract()
