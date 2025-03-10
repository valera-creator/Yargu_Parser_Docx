# pip install easyocr
# pip install pdf2image
import easyocr
from pdf2image import convert_from_path
from common_functions import check_correct_file, write_text, parse_terminal, check_correct_data
import torch
import os
import re


def recognize_text_easy_ocr(path_pdf_file, path_image, reader, cur_page, method):
    """
    из картинки с помощью библиотеки pytesseract распознается текст и записывается в файл.txt

    :param path_pdf_file: путь к pdf файлу
    :param path_image: путь к картинке, с которой будет распознаваться текст
    :param reader: объект reader для распознавания
    :param cur_page:  текущая страница документа
    :param method: метод распознавания (ocr/tesseract)
    """

    print(f'Начало {cur_page} Страницы{"_" * 50}')
    text = reader.readtext(
        image=path_image,  # путь к изображению
        paragraph=True,  # объединение в параграфы
        detail=0,  # детализация: с 0 вернется только текст
        mag_ratio=1.5,  # коэффициент увеличения изображения
        add_margin=0.1,  # добавление маргина для улучшения распознавания
        min_size=1,  # минимальный размер текстового блока
        beamWidth=7,  # ширина лучевого поиска (чем больше, тем точнее)
    )

    # запись в файл
    write_text(path_pdf_file, f'\nНачало {cur_page} Страницы{"_" * 50}\n', method)
    for elem in text:
        elem = re.sub(r'(\w)-\s(\w)', r'\1\2', elem)
        elem = re.sub(r'(\w+)\s*-\s*(\w+)', r'\1\2', elem)
        write_text(path_pdf_file, f'{elem.strip()}\n', method)
    write_text(path_pdf_file, f'\nКонец {cur_page} Страницы{"_" * 50}\n', method)

    print(f'Конец {cur_page} Страницы{"_" * 50}\n')


def convert_pdf_to_images(first_page, last_page, path_pdf_file, image_folder, reader, method):
    """
    pdf файл конвертируется, а после
    из каждой страницы файла получается картинка,
    которая передается потом в функцию recognize_text для распознавания текста

    :param first_page: первая страница документа, с которой получать текст
    :param last_page: последняя страница документа, до которой получать текст
    :param path_pdf_file: путь к pdf файлу
    :param image_folder: путь, где будут лежать картинки-страницы pdf файла
    :param reader - объект reader для распознавания
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
        recognize_text_easy_ocr(path_pdf_file, path_save, reader, cur_page, method)
        os.remove(path_save)


def main():
    """
    перед запуском программы настройте это:

    image_folder - путь, где будут лежать картинки-страницы pdf файла
    (после распознавания текста они удаляются) и файл.txt с текстом
    method = [e] - с помощью easyocr

    first_page - первая страница документа, с которой получать текст
    last_page - последняя страница документа, до которой получать текст
    languages - языки, которые могут быть в файле
    path_pdf_file - путь к pdf файлу
    """

    image_folder = 'test_files'
    method = '[e]'

    first_page, last_page, languages, path_pdf_file = parse_terminal()
    check_correct_data(lang=languages, path=path_pdf_file, first_page=first_page, last_page=last_page,
                       is_check_lang=True)

    print('проверка доступа gpu...')
    gpu = True if torch.cuda.is_available() else False

    print('запуск reader...')
    reader = easyocr.Reader(languages, gpu=gpu)

    print(f'работа с файлом...')
    check_correct_file(path_pdf_file)
    convert_pdf_to_images(first_page, last_page, path_pdf_file, image_folder, reader, method)


if __name__ == "__main__":
    main()
