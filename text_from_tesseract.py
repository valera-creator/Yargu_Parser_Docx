# pip install pytesseract
# python.exe -m pip install --upgrade pip
# pip install pdf2image

from PIL import Image
from pdf2image import convert_from_path
from common_functions import check_correct_file, write_text, parse_terminal, check_correct_data
import pytesseract
import os


def recognize_text_tesseract(path_pdf_file, path_file, languages, cur_page, method):
    """
    из картинки с помощью библиотеки pytesseract распознается текст и записывается в файл.txt

    :param path_pdf_file: путь к pdf файлу
    :param path_file: путь к картинке, с которой будет распознаваться текст
    :param languages: языки, которые будут искаться
    :param cur_page:  текущая страница документа
    :param method: метод распознавания (ocr/tesseract)
    """

    print(f'Начало {cur_page} Страницы{"_" * 50}')
    im = Image.open(path_file)
    text = str(pytesseract.image_to_string(im, lang=languages)).strip()

    # запись в файл
    write_text(path_pdf_file, f'\nНачало {cur_page} Страницы{"_" * 50}\n', method)
    write_text(path_pdf_file, text, method)
    write_text(path_pdf_file, f'\nКонец {cur_page} Страницы{"_" * 50}\n', method)
    print(f'Конец {cur_page} Страницы{"_" * 50}\n')


def convert_pdf_to_images(first_page, last_page, path_pdf_file, image_folder, languages, method):
    """
    pdf файл конвертируется, а после
    из каждой страницы файла получается картинка,
    которая передается потом в функцию recognize_text для распознавания текста

    :param first_page: первая страница документа, с которой получать текст
    :param last_page: последняя страница документа, до которой получать текст
    :param path_pdf_file: путь к pdf файлу
    :param image_folder: путь, где будут лежать картинки-страницы pdf файла
    :param languages: языки, которые могут быть в файле
    :param method: метод распознавания (ocr/tesseract)
    """

    images = convert_from_path(path_pdf_file, first_page=first_page, last_page=last_page, dpi=300)
    for i, image in enumerate(images):
        if first_page is None:
            cur_page = i + 1
        else:
            cur_page = first_page + i
        path_save = os.path.join(image_folder, f"page_{cur_page}.png")
        image.save(path_save, "PNG")
        recognize_text_tesseract(path_pdf_file, path_save, languages, cur_page, method)
        os.remove(path_save)


def main():
    """
    перед запуском программы настройте это:

    image_folder - путь, где будут лежать картинки-страницы pdf файла
    (после распознавания текста они удаляются) и файл.txt с текстом
    method = [t] - с помощью tesseract

    first_page - первая страница документа, с которой получать текст
    last_page - последняя страница документа, до которой получать текст
    languages - языки, которые могут быть в файле
    path_pdf_file - путь к pdf файлу
    """

    image_folder = 'test_files'
    method = '[t]'

    first_page, last_page, languages, path_pdf_file = parse_terminal()
    languages = '+'.join(languages)

    check_correct_data(lang=languages, path=path_pdf_file, first_page=first_page, last_page=last_page,
                       is_check_lang=True)
    check_correct_file(path_pdf_file)
    convert_pdf_to_images(first_page, last_page, path_pdf_file, image_folder, languages, method)


if __name__ == "__main__":
    main()
