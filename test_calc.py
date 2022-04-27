import math
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import NoSuchElementException

desired_caps = dict(
    platformName='Android',
    app='C:\\drom\\app-debug.apk'    # path to file
)

driver = webdriver.Remote(command_executor='http://localhost:4723/wd/hub', desired_capabilities=desired_caps)

try:
    driver.find_element(by=AppiumBy.ID, value='android:id/button1').click()  # close window message old version app
except NoSuchElementException as e:
    print(e)


def round2(n):  # rounding to the second decimal place
    return math.floor(n * 100 + 0.5) / 100


def calculate_answer(left, right, sign):
    res = 0
    left = float(left)
    right = float(right)
    if sign == '+':
        res = left + right
    if sign == '-':
        res = left - right
    if sign == '*':
        res = left * right
    if sign == '/':
        res = left / right
    return ("{:.2f} " + sign + " {:.2f} = {:.2f}").format(round2(left), round2(right), round2(res))


def calculate_test(left, right, sign, answer=None):
    input_left = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value='inputFieldLeft')
    input_left.clear()
    input_left.send_keys(left)

    input_right = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value='inputFieldRight')
    input_right.clear()
    input_right.send_keys(right)

    buttons = {
        '+': 'additionButton',
        '*': 'multiplicationButton',
        '/': 'divisionButton',
        '-': 'subtractButton'
    }

    button = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value=buttons[sign])  # Button operation
    button.click()

    result = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value='resultTextView')

    if not answer:
        answer = calculate_answer(left, right, sign)

    print(result.text)
    print(answer)
    assert result.text == answer


def test_add():
    calculate_test(300.000, 500.000, '+')  # 800.00 - true


def test_sub():
    calculate_test(300, 500.00, '-')  # 1600.00 - false - ошибка логики работы


def test_sub_min():
    calculate_test(2, 2, '-')  # 8.00 - false - ошибка логики работы


def test_mult():
    calculate_test(300, 500, '*')  # 150000.00 - true


def test_div():
    calculate_test(300, 500, '/')  # 0.60 - true


def test_add_mines():
    calculate_test(-10, +20, '+')  # 10.00 - true


def test_mult_minus():
    calculate_test(-10, 30, '*')  # -300.00 - true


def test_div_zero():
    calculate_test(-0, 555, '/')  # 0.00 - true


def test_div_zero_zero():
    calculate_test(0, 0, '/', 'NaN')  # NaN - false - должна выпадать ошибка


def test_mult_min():
    calculate_test(8, 4, '*')  # 32.00 - true


def test_add_str_str_int():
    calculate_test('123', '321', '+')  # 444.00 - true


def test_mult_str():
    calculate_test('123', 321, '*')  # 39483.00 - true


def test_dev_str():
    calculate_test(123, '321', '/')  # 0.38 - true


def test_mult_bigInt():
    calculate_test(12345678987654321, 5,
                   '*')  # 61728395259543552.00 (61728394938271605) - false - ошибка вычисления больших чисел

def test_add_bigInt():
    calculate_test(123123123, 321321321, '+')    # 444444416.00  (444444444)  - false


def test_div_by_zero():
    calculate_test(555, 0, '/', 'Infinity')  # Infinity - true


def test_mult_str_int():
    calculate_test('qwerty', 12, '*',
                   'Please, fill the input fields correctly')  # Please, fill the input fields correctly - true


def test_mult_by_str():
    calculate_test(12, 'qwerty', '*',
                   'Please, fill the input fields correctly')  # Please, fill the input fields correctly - true


def test_add_str_str():
    calculate_test('qwe', 'rty', '+',
                   'Please, fill the input fields correctly')  # Please, fill the input fields correctly - true


def test_div_min():
    calculate_test(0.010000001, 100000, '/')  # 0.00 - true

def test_div_min_min():
    calculate_test(0.0001, 0.001, '-')    # 0.00 - false


def test_none_str():
    calculate_test(' ', 123, '*', 'Please, fill the input fields correctly')  # Please, fill the input fields correctly


def test_mult_minus_minus():
    calculate_test(-0.01, -1000, '*')  # 10.00 - true


def test_add_minus_minus():
    calculate_test(-0.01, -1000, '+')  # -1000.01 - true


def test_sub_minus_minus():
    calculate_test(-0.01, -1000, '-')  # -2000.02 - false - ошибка логики работы, работает по формуле (a + b) * 2


def test_div_minus_minus():
    calculate_test(-0.01, -1000, '/')  # 0.00 - false - не работает после 2 знаков после запятой


def test_add_minus_min():
    calculate_test(-0.11, 1000, '+')  # 999.89 - true
