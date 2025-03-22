# pip install tqdm
from tqdm import tqdm
from common_functions import parse_terminal, check_correct_data


def gef_function(method):
    """Импортирует и возвращает функцию для обработки текста в зависимости от выбранного метода."""
    match method:
        case 'l':
            from text_from_layer_pdf import receive_text_from_layer
            return receive_text_from_layer
        case 'e':
            from text_from_easy_ocr import start_easy_ocr
            return start_easy_ocr
        case 't':
            from text_from_tesseract import start_tesseract
            return start_tesseract


def customize_progress_bar_for_pages(progress_bar):
    """настройка значений progressbar под страницы"""
    progress_bar.total = 0
    progress_bar.desc = 'Обработка страниц'
    progress_bar.unit = 'page'
    progress_bar.colour = 'green'


def main():
    """
    Функция:
    1. Получает данные из командной строки с помощью функции parse_terminal().
    2. Проверяет корректность переданного пути к файлу с помощью check_correct_file().
    3. В зависимости от выбранного метода (method) импортируется библиотека и распознается текст выбранным методотом

    Аргументы:
    first_page - номер первой страницы для обработки
    last_page - номер последней страницы для обработки (включительно)
    languages - языки для распознавания в документе
    path - путь к pdf файлу
    method - метод распознавания текста.
    progress_bar - объект progressbar для отображения процесса показа
    process_function - функция для распознавания

    Допустимые значения method:
    1. 'l' (layer): Встроенный метод извлечения текста из PDF.
    2. 'e' (EasyOCR): Использование библиотеки EasyOCR.
    3. 't' (Tesseract): Использование библиотеки Tesseract.
    """

    first_page, last_page, languages, path, method = parse_terminal()
    check_correct_data(first_page, last_page, method, path)
    progress_bar = tqdm(desc="Загрузка модулей...", unit="iter", colour='blue')
    process_function = gef_function(method=method)
    customize_progress_bar_for_pages(progress_bar)

    if method == 'l':
        process_function(first_page=first_page, last_page=last_page, path_pdf_file=path, progress_bar=progress_bar)
    elif method in ['t', 'e']:
        process_function(first_page=first_page, last_page=last_page, path_pdf_file=path, languages=languages,
                         progress_bar=progress_bar)

    progress_bar.close()


if __name__ == "__main__":
    main()
