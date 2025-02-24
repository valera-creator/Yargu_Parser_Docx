# pip install pytesseract
# python.exe -m pip install --upgrade pip
# pip install pdf2image

from PIL import Image
from pdf2image import convert_from_path
import pytesseract
import os


def check_correct_file(path_file):
    """проверка на то что файл существует и является pdf"""
    if not os.path.exists(path_file):
        quit(f"Ошибка: pdf файл по пути {path_file} не найден.")
    if not path_file.endswith('.pdf'):
        quit('Ошибка: файл должен иметь расширение .pdf')


def write_text(path_pdf_file, text):
    """запись текста в текстовый файл с названием pdf документа, но с расширением .txt"""
    path_file_txt = os.path.splitext(path_pdf_file)[0] + '.txt'
    with open(path_file_txt, mode='a', encoding='utf-8') as file:
        file.write(text)


def recognize_text_tesseract(path_pdf_file, path_file, languages, cur_page):
    """
    из картинки с помощью библиотеки pytesseract распознается текст и записывается в файл.txt

    :param path_pdf_file: путь к pdf файлу
    :param path_file: путь к картинке, с которой будет распознаваться текст
    :param languages: языки, которые будут искаться
    :param cur_page:  текущая страница документа (отсчет идет от кол-ва распрарсенных страниц, а не с книжных страниц)
    """

    print(f'Начало {cur_page} Страницы{"_" * 50}')
    im = Image.open(path_file)
    text = str(pytesseract.image_to_string(im, lang=languages)).strip()

    # запись в файл
    write_text(path_pdf_file, f'\nНачало {cur_page} Страницы{"_" * 50}\n')
    write_text(path_pdf_file, text)
    write_text(path_pdf_file, f'\nКонец {cur_page} Страницы{"_" * 50}\n')
    print(f'Конец {cur_page} Страницы{"_" * 50}\n')


def convert_pdf_to_images(path_pdf_file, output_folder, languages):
    """
    pdf файл конвертируется, а после
    из каждой страницы файла получается картинка,
    которая передается потом в функцию recognize_text для распознавания текста

    :param path_pdf_file: путь к pdf файлу
    :param output_folder: путь, где будут лежать картинки-страницы pdf файла
    :param languages: языки, которые могут быть в файле
    """

    images = convert_from_path(path_pdf_file, first_page=1, last_page=5, dpi=300)
    for i, image in enumerate(images):
        path_save = os.path.join(output_folder, f"page_{i + 1}.png")
        image.save(path_save, "PNG")
        recognize_text_tesseract(path_pdf_file, path_save, languages, i + 1)
        os.remove(path_save)


def main():
    """
    перед запуском программы настройте это:

    path_pdf_file - путь к pdf файлу
    out_folder - путь, где будут лежать картинки-страницы pdf файла
    (после распознавания текста они удаляются) и файл.txt с текстом
    languages_for_doc - языки, которые могут быть в файле
    """

    path_pdf_file = os.path.join('test_files', 'file_1.pdf')
    out_folder = 'test_files'
    languages_for_doc = 'eng+rus'

    check_correct_file(path_pdf_file)
    convert_pdf_to_images(path_pdf_file, out_folder, languages_for_doc)


if __name__ == "__main__":
    main()
