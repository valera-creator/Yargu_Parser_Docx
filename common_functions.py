import os
import argparse


def check_correct_file(path_file):
    """проверка на то что файл существует и является pdf"""
    if not os.path.exists(path_file):
        quit(f"Ошибка: pdf файл по пути {path_file} не найден.")
    if not path_file.endswith('.pdf'):
        quit('Ошибка: файл должен иметь расширение .pdf')


def check_correct_data(lang, path):
    """
    функция проверяет корректность переданных данных
    :param lang: язык в документе
    :param path: путь к pdf-файлу

    """
    if not lang:
        quit('передайте язык/языки, который/которые нужно распознать в документе')
    if path is None:
        quit('передайте путь к файлу, откуда нужно достать текст')


def write_text(path_pdf_file, text, method):
    """запись текста в текстовый файл с названием pdf документа, но с расширением .txt"""
    path_file_txt = os.path.splitext(path_pdf_file)[0] + '.txt'
    path_file_txt = os.path.basename(path_file_txt)
    path_file_txt = method + path_file_txt
    path_file_txt = os.path.join('results', path_file_txt)
    with open(path_file_txt, mode='a', encoding='utf-8') as file:
        file.write(text)


def parse_terminal():
    """получение данных с терминала через библиотеку argparse"""
    # примеры запусков программы через терминал:
    # python text_from_tesseract.py --languages rus eng --path test_files/file_1.pdf --first_page 1 --last_page 5
    # python text_from_easy_ocr.py --languages ru en --path test_files/file_1.pdf --first_page 1 --last_page 5

    parser = argparse.ArgumentParser()
    parser.add_argument('--first_page', default=None, type=int)
    parser.add_argument('--last_page', default=None, type=int)
    parser.add_argument('--languages', nargs="*", default=['en', 'ru'])
    parser.add_argument('--path', type=str)

    args = parser.parse_args()
    return args.first_page, args.last_page, args.languages, args.path
