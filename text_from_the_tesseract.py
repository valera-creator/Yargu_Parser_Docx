# pip install pytesseract
# python.exe -m pip install --upgrade pip
# pip install pdf2image

from PIL import Image
from pdf2image import convert_from_path
from common_functions import check_correct_file, write_text, parse_terminal
import pytesseract
import os


def recognize_text_tesseract(path_pdf_file, path_file, languages, cur_page, method):
    """
    из картинки с помощью библиотеки pytesseract распознается текст и записывается в файл.txt

    :param path_pdf_file: путь к pdf файлу
    :param path_file: путь к картинке, с которой будет распознаваться текст
    :param languages: языки, которые будут искаться
    :param cur_page:  текущая страница документа (отсчет идет от кол-ва распрарсенных страниц, а не с книжных страниц)
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


def convert_pdf_to_images(path_pdf_file, output_folder, languages, method):
    """
    pdf файл конвертируется, а после
    из каждой страницы файла получается картинка,
    которая передается потом в функцию recognize_text для распознавания текста

    :param path_pdf_file: путь к pdf файлу
    :param output_folder: путь, где будут лежать картинки-страницы pdf файла
    :param languages: языки, которые могут быть в файле
    :param method: метод распознавания (ocr/tesseract)
    """

    images = convert_from_path(path_pdf_file, first_page=1, last_page=5, dpi=300)
    for i, image in enumerate(images):
        path_save = os.path.join(output_folder, f"page_{i + 1}.png")
        image.save(path_save, "PNG")
        recognize_text_tesseract(path_pdf_file, path_save, languages, i + 1, method)
        os.remove(path_save)


def main():
    """
    перед запуском программы настройте это:

    path_pdf_file - путь к pdf файлу
    out_folder - путь, где будут лежать картинки-страницы pdf файла
    (после распознавания текста они удаляются) и файл.txt с текстом
    languages_for_doc - языки, которые могут быть в файле
    method = [t] - с помощью tesseract
    """

    path_pdf_file = os.path.join('test_files', 'file_1.pdf')
    out_folder = 'test_files'
    languages_for_doc = 'eng+rus'
    method = '[t]'

    check_correct_file(path_pdf_file)
    convert_pdf_to_images(path_pdf_file, out_folder, languages_for_doc, method)


if __name__ == "__main__":
    main()
