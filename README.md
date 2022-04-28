# Тестовое окружение для Windows 10 x64
Требования:
1.	Python 3.10 (https://www.python.org/downloads/)
2.	Appium Server GUI windows 1.22.3 (https://appium.io/downloads.html)
3.	Genymotion Desktop 3.2.1 (https://www.genymotion.com/download/)
4.	PyTest (https://docs.pytest.org/en/7.1.x/getting-started.html)

В Genymotion Desktop добавить эмулятор устройства Google Pixel 3  с версией Android 10.

Поместить  файлы test_calc.py, app-debug.apk в папку C:\drom.

Запустить эмулятор Google Pixel 3  

Запустить Appium Server

Из папки «C:\drom» выполнить pytest
