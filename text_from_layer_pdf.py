# pip install pdfplumber

import pdfplumber
from common_functions import write_text


def convert_num_pages(first_page, last_page, pdf):
    """
     Функция преобразует номера первой и последней страницы для корректной работы с индексацией Python.

    :param first_page: номер первой страницы для получения текста
    :param last_page: номер последней страницы для получения текста (включительно)
    :param pdf: список со объектами страниц pdf

    :return: преобразованное под индексацию значение первой и последней страницы
    """

    if first_page is None:  # первая страница не передана, делаем индексацию под питон
        first_page = 0
    else:
        first_page -= 1  # индексация в цикл

    if last_page is None:  # посл страница не передана, текст будет распознаваться до последней страницы (включительно)
        last_page = len(pdf.pages)
    elif last_page > len(pdf.pages):  # случай, если передали страниц больше, чем их в документе
        last_page = len(pdf.pages)

    return first_page, last_page


def receive_text_from_layer(path_pdf_file, first_page, last_page, progress_bar):
    """
    Функция извлекает текст из указанных страниц PDF-файла и записывает его в текстовый файл.
    Результат записывается в текстовый файл с тем же именем, что и PDF-файл, но с расширением .txt.

    :param path_pdf_file: путь к pdf файлу
    :param first_page: первая страница
    :param last_page: последняя страница
    :param progress_bar: progressbar для отображения прогресса обработанных страниц

    method - метод получения текста (в данном случае с помощью доставания текстового слоя, [l])
    """

    method = '[l]'
    with pdfplumber.open(path_pdf_file) as pdf:
        first_page, last_page = convert_num_pages(first_page, last_page, pdf)
        progress_bar.total = last_page - first_page

        for page in range(first_page, last_page):
            text = pdf.pages[page].extract_text()
            write_text(path_pdf_file, f'\nНачало страницы {page + 1}{"_" * 50}\n', method)
            write_text(path_pdf_file, text, method)
            write_text(path_pdf_file, f'\nКонец страницы {page + 1}{"_" * 50}\n', method)

            progress_bar.update(1)
