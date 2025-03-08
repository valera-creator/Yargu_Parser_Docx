from common_functions import parse_terminal, check_correct_data, check_correct_file
from text_from_layer_pdf import receive_text
from text_from_easy_ocr import start_easy_ocr


def main():
    """
    функция получает даннные, считанный с командной строки, затем проверяет существование файла и по переданному
    методу вызывается функция распознавания текста

    first_page - первая страница
    last_page - последняя страница
    languages - языки
    path - путь к pdf файлу
    method - метод распознавания [l, t, e]
    """

    first_page, last_page, languages, path, method = parse_terminal()
    check_correct_file(path)

    if method == 'l':
        check_correct_data(first_page, last_page)
        receive_text(path, first_page, last_page)

    elif method == 'e':
        check_correct_data(first_page, last_page, lang=languages, is_check_lang=True)
        start_easy_ocr(path, first_page, last_page, languages)

    elif method == 't':
        pass  # реализуется попозже

    else:
        print('метод распознавания не найден')


if __name__ == "__main__":
    main()
