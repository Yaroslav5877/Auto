import pytest
from selenium import webdriver
from lesson_7.Calculator.Calcmainpage import CalcMain

@pytest.fixture
def chrome_browser():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

def test_calculator_assert(chrome_browser):
    calcmain = CalcMain(chrome_browser)
    calcmain.insert_time()
    calcmain.clicking_buttons()
    result_text = calcmain.wait_button_gettext()
    assert "15" in result_text
