<p>
Программа реализовывалась на Windows.<br>
Для запуска программы необходимо перейти по 
<a href="https://tesseract-ocr.github.io/tessdoc/Installation.html">ссылке</a> и скачать к себе эту программу.<br>

Для Windows <a href="https://github.com/UB-Mannheim/tesseract/wiki"> отсюда скачать программу</a>.<br>
Во время установки не забывайте выбрать языки, которые вам будут нужны. Это настраивается в Additional language data.<br>
Далее необходимо в переменных среды прописать путь к папке, в которую мы ставили ранее скачанную программу.<br>

Для установки библиотек: 
```
pip install -r requirements.txt
```

При установки может выдаваться в терминале что-то по типу "A new release of pip is available:", тогда просто введите предложенную команду для обновления pip.<br>
Команды также написаны в верху файла text_from_the_image.py.<br>

</p>