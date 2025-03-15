import os
import argparse


def check_correct_data(first_page, last_page, method, path_file):
    """
    функция проверяет корректность переданных данных и существование pdf файла
    :param first_page: первая страница, с которой распознавать текст
    :param last_page: последняя страница, до которой распознавать текст (включительно)
    :param method: метод распознавания
    :param path_file: путь к pdf файлу
    """

    if first_page is not None and last_page is not None and first_page > last_page:
        quit('ошибка: номер последней страницы меньше первой')
    if first_page is not None and first_page < 0:
        quit('ошибка: номер первой страницы < 0')
    if last_page is not None and last_page < 0:
        quit('ошибка: номер последней страницы < 0')
    if method not in ['l', 'e', 't']:
        quit('ошибка: метод распознавания не найден среди "l", "e", "t"')
    if not os.path.exists(path_file):
        quit(f"Ошибка: pdf файл по пути {path_file} не найден.")
    if not path_file.endswith('.pdf'):
        quit('Ошибка: файл должен иметь расширение .pdf')


def write_text(path_pdf_file, text, method):
    """
    запись текста в текстовый файл с названием pdf документа, но с расширением .txt
    :param path_pdf_file: путь к pdf файлу
    :param text: текст, который надо записать
    :param method: приписывание к названию файла метода, с помощью которого был получен текст
    """

    path_file_txt = os.path.splitext(path_pdf_file)[0] + '.txt'
    path_file_txt = os.path.basename(path_file_txt)
    path_file_txt = method + path_file_txt
    path_file_txt = os.path.join('results', path_file_txt)
    with open(path_file_txt, mode='a', encoding='utf-8') as file:
        file.write(text)


def parse_terminal():
    """получение данных с терминала через библиотеку argparse"""
    # примеры запусков программы через терминал:
    # python main.py --path test_files/file.pdf --method e --first_page 1 --last_page 5
    # python main.py --path test_files/file.pdf --method t --first_page 1 --last_page 5
    # python main.py --path test_files/file.pdf --method l --first_page 1 --last_page 5

    parser = argparse.ArgumentParser()
    parser.add_argument('--first_page', default=None, type=int)
    parser.add_argument('--last_page', default=None, type=int)
    parser.add_argument('--languages', nargs="*", default=['en', 'ru'])
    parser.add_argument('--path', type=str, default='')
    parser.add_argument('--method', type=str, default='')

    args = parser.parse_args()
    return args.first_page, args.last_page, args.languages, args.path, args.method.lower()
