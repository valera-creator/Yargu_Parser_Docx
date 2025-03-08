# pip install pdfplumber
import pdfplumber
from common_functions import write_text


def convert_num_pages(first_page, last_page, pdf):
    """
    функция подстраивает по питон значения номеров первой и последней страницы

    :param first_page: первая страница для получения текста
    :param last_page: последняя страница для получения текста (включительно)
    :param pdf: список со объектами

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


def receive_text(path_pdf, first_page, last_page):
    """
    функция получает текст со страниц и записывает его в txt файл

    :param path_pdf: путь к pdf файлу
    :param first_page: первая страница
    :param last_page: последняя страница
    method - метод получения текста (в данном случае с помощью доставания текстового слоя, [l])
    """

    method = '[l]'
    with pdfplumber.open(path_pdf) as pdf:
        first_page, last_page = convert_num_pages(first_page, last_page, pdf)

        for page in range(first_page, last_page):
            print(f'\nНачало страницы {page + 1} {"_" * 50}')

            text = pdf.pages[page].extract_text()
            write_text(path_pdf, f'\nНачало страницы {page + 1}{"_" * 50}\n', method)
            write_text(path_pdf, text, method)
            write_text(path_pdf, f'\nКонец страницы {page + 1}{"_" * 50}\n', method)

            print(f'Конец страницы {page + 1} {"_" * 50}\n')
