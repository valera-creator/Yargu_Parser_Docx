import os


def check_correct_file(path_file):
    """проверка на то что файл существует и является pdf"""
    if not os.path.exists(path_file):
        quit(f"Ошибка: pdf файл по пути {path_file} не найден.")
    if not path_file.endswith('.pdf'):
        quit('Ошибка: файл должен иметь расширение .pdf')


def write_text(path_pdf_file, text, method):
    """запись текста в текстовый файл с названием pdf документа, но с расширением .txt"""
    path_file_txt = os.path.splitext(path_pdf_file)[0] + '.txt'
    path_file_txt = os.path.basename(path_file_txt)
    path_file_txt = method + path_file_txt
    path_file_txt = os.path.join('results', path_file_txt)
    with open(path_file_txt, mode='a', encoding='utf-8') as file:
        file.write(text)
