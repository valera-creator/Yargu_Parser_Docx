# pip install pytesseract
# python.exe -m pip install --upgrade pip

from PIL import Image
import pytesseract


def recognize():
    """
    первым аргументом идет путь к картинке
    в lang передаются языки, которые будут распознаваться
    """
    print(str(pytesseract.image_to_string(Image.open('test_files/b2.png'), lang='eng+rus')).strip())


if __name__ == "__main__":
    recognize()
