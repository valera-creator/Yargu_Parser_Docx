# pip install easyocr
# pip install pdf2image
import easyocr
from pdf2image import convert_from_path
from common_functions import check_correct_file, write_text
import torch
import os
import re


def recognize_text_easy_ocr(path_pdf_file, path_image, reader, cur_page, method):
    """
    из картинки с помощью библиотеки pytesseract распознается текст и записывается в файл.txt

    :param path_pdf_file: путь к pdf файлу
    :param path_image: путь к картинке, с которой будет распознаваться текст
    :param reader: объект reader для распознавания
    :param cur_page:  текущая страница документа (отсчет идет от кол-ва распрарсенных страниц, а не с книжных страниц)
    :param method: метод распознавания (ocr/tesseract)
    """

    print(f'Начало {cur_page} Страницы{"_" * 50}')
    text = reader.readtext(
        image=path_image,  # путь к изображению
        paragraph=True,  # объединение в параграфы
        detail=0,  # детализация: с 0 вернется только текст
    )

    # запись в файл
    write_text(path_pdf_file, f'\nНачало {cur_page} Страницы{"_" * 50}\n', method)
    for elem in text:
        elem = re.sub(r'(\w)-\s(\w)', r'\1\2', elem)
        elem = re.sub(r'(\w+)\s*-\s*(\w+)', r'\1\2', elem)
        write_text(path_pdf_file, f'{elem.strip()}\n', method)
    write_text(path_pdf_file, f'\nКонец {cur_page} Страницы{"_" * 50}\n', method)

    print(f'Конец {cur_page} Страницы{"_" * 50}\n')


def convert_pdf_to_images(path_pdf_file, output_folder, reader, method):
    """
    pdf файл конвертируется, а после
    из каждой страницы файла получается картинка,
    которая передается потом в функцию recognize_text для распознавания текста

    :param path_pdf_file: путь к pdf файлу
    :param output_folder: путь, где будут лежать картинки-страницы pdf файла
    :param reader - объект reader для распознавания
    :param method: метод распознавания (ocr/tesseract)
    """

    images = convert_from_path(path_pdf_file, first_page=1, last_page=10, dpi=300)
    for i, image in enumerate(images):
        path_save = os.path.join(output_folder, f"page_{i + 1}.png")
        image.save(path_save, "PNG")
        recognize_text_easy_ocr(path_pdf_file, path_save, reader, i + 1, method)
        os.remove(path_save)


def main():
    """
    перед запуском программы настройте это:

    path_pdf_file - путь к pdf файлу
    out_folder - путь, где будут лежать картинки-страницы pdf файла
    (после распознавания текста они удаляются) и файл.txt с текстом
    languages_for_doc - языки, которые могут быть в файле
    method = '[e]' - с помощью easyocr
    """

    path_pdf_file = os.path.join('test_files', 'file_1.pdf')
    out_folder = 'test_files'
    languages_for_doc = ['ru', 'en']
    method = '[e]'

    print('проверка доступа gpu...')
    gpu = True if torch.cuda.is_available() else False

    print('запуск reader...')
    reader = easyocr.Reader(languages_for_doc, gpu=gpu)

    print(f'работа с файлом...')
    check_correct_file(path_pdf_file)
    convert_pdf_to_images(path_pdf_file, out_folder, reader, method)


if __name__ == "__main__":
    main()
