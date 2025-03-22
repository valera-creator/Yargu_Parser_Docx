# pip install pytesseract
# python.exe -m pip install --upgrade pip
# pip install pdf2image

from PIL import Image
from pdf2image import convert_from_path
from common_functions import write_text
import pytesseract
import os


def recognize_text_tesseract(path_pdf_file, path_file, languages, cur_page, method):
    """
    Из картинки с помощью библиотеки pytesseract распознается текст и записывается в файл.txt

    :param path_pdf_file: путь к pdf файлу
    :param path_file: путь к картинке, с которой будет распознаваться текст
    :param languages: языки, которые будут искаться
    :param cur_page:  текущая страница документа
    :param method: метод распознавания (например, [t] для tesseract)
    """

    im = Image.open(path_file)
    text = str(pytesseract.image_to_string(im, lang=languages)).strip()

    # запись в файл
    write_text(path_pdf_file, f'\nНачало {cur_page} Страницы{"_" * 50}\n', method)
    write_text(path_pdf_file, text, method)
    write_text(path_pdf_file, f'\nКонец {cur_page} Страницы{"_" * 50}\n', method)


def convert_pdf_to_images(first_page, last_page, path_pdf_file, image_folder, languages, method, progress_bar):
    """
    Функция конвертирует страницы PDF-файла в изображения и распознает текст с каждой страницы,
    передавая в функцию recognize_text изображения и другие параметры для распознавания текста

    :param first_page: первая страница документа, с которой получать текст
    :param last_page: последняя страница документа, до которой получать текст
    :param path_pdf_file: путь к pdf файлу
    :param image_folder: путь, где будут лежать картинки-страницы pdf файла
    :param languages: языки, которые могут быть в файле
    :param method: метод распознавания (например, [t] для tesseract)
    :param progress_bar: progressbar для отображения прогресса обработанных страниц
    """

    images = convert_from_path(path_pdf_file, first_page=first_page, last_page=last_page, dpi=300)
    progress_bar.total = len(images)

    for i, image in enumerate(images):
        if first_page is None:
            cur_page = i + 1
        else:
            cur_page = first_page + i
        path_save = os.path.join(image_folder, f"page_{cur_page}.png")
        image.save(path_save, "PNG")
        recognize_text_tesseract(path_pdf_file, path_save, languages, cur_page, method)
        os.remove(path_save)
        progress_bar.update(1)


def start_tesseract(path_pdf_file, first_page, last_page, languages, progress_bar):
    """
    Функция инициализирует процесс конвертации PDF-файла в изображения и распознавания текста
    с помощью библиотеки pytesseract. Распознанный текст записывается в текстовый файл.

    image_folder - путь, где будут лежать картинки-страницы pdf файла
    (после распознавания текста они удаляются) и файл.txt с текстом
    method - метод распознавания текста

    :param path_pdf_file: путь к pdf файлу
    :param first_page: первая страница, с которой распознавать текст
    :param last_page: последняя страница, до которой распознавать текст (включительно)
    :param languages: языки, которые искать в документе
    :param progress_bar: progressbar для отображения прогресса обработанных страниц
    """

    image_folder = 'test_files'
    method = '[t]'
    languages = 'rus+eng' if sorted(languages) == ['en', 'ru'] else '+'.join(languages)

    convert_pdf_to_images(first_page, last_page, path_pdf_file, image_folder, languages, method, progress_bar)
