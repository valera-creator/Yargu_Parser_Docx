from common_functions import parse_terminal, check_correct_data, check_correct_file


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

    Допустимые значения method:
    1. 'l' (layer): Встроенный метод извлечения текста из PDF.
    2. 'e' (EasyOCR): Использование библиотеки EasyOCR.
    3. 't' (Tesseract): Использование библиотеки Tesseract.
    """

    first_page, last_page, languages, path, method = parse_terminal()
    check_correct_file(path)

    if method == 'l':
        from text_from_layer_pdf import receive_text
        check_correct_data(first_page, last_page)
        receive_text(path, first_page, last_page)

    elif method == 'e':
        from text_from_easy_ocr import start_easy_ocr
        check_correct_data(first_page, last_page, lang=languages, is_check_lang=True)
        start_easy_ocr(path, first_page, last_page, languages)

    elif method == 't':
        from text_from_tesseract import start_tesseract
        check_correct_data(first_page, last_page, lang=languages, is_check_lang=True)
        start_tesseract(path, first_page, last_page, languages)

    else:
        print('метод распознавания не найден')


if __name__ == "__main__":
    main()
