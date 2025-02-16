# pip install pytesseract
# python.exe -m pip install --upgrade pip
# pip install pdf2image

from PIL import Image
from pdf2image import convert_from_path
import pytesseract
import os


def recognize_text(path_file, languages, cur_page):
    """
    из картинки с помощью библиотеки pytesseract распознается текст и печатается на экран (пока что на экран)

    :param path_file: путь к картинке, с которой будет распознаваться текст
    :param languages: языки, которые будут искаться
    :param cur_page:  текущая страница документа
    """

    print(f'{cur_page}) {"_" * 30}')
    print(str(pytesseract.image_to_string(Image.open(path_file), lang=languages)).strip())
    print('\n\n')


def convert_pdf_to_images(path_pdf, output_folder, languages):
    """
    из каждой страницы файла получается картинка,
    которая передается потом в функцию recognize_text для распознавания текста

    :param path_pdf: путь к pdf файлу
    :param output_folder: путь, где будут лежать картинки-страницы pdf файла
    :param languages: языки, которые могут быть в файле
    """

    images = convert_from_path(path_pdf, first_page=1, last_page=5, dpi=300)
    for i, image in enumerate(images):
        path_save = os.path.join(output_folder, f"page_{i + 1}.png")
        image.save(path_save, "PNG")
        recognize_text(path_save, languages, i + 1)
        os.remove(path_save)


def main():
    """
     pdf_file - путь к pdf файлу
     out_folder - путь, где будут лежать картинки-страницы pdf файла
     languages_for_doc - языки, которые могут быть в файле
    """

    path_pdf_file = os.path.join('test_files', 'file_1.pdf')
    out_folder = 'test_files'
    languages_for_doc = 'eng+rus'
    convert_pdf_to_images(path_pdf_file, out_folder, languages_for_doc)


if __name__ == "__main__":
    main()
