from lesson_7.Swag_Labs.Shopmain import ShopmainPage
from lesson_7.Swag_Labs.Shopcontainer import ShopContainer
import time

def test_shop(chrome_browser):
    expected_total = "58.29"

    shopmain = ShopmainPage(chrome_browser)
    shopmain.reristration_field()
    shopmain.buy_issue()
    shopmain.click_issue()
    shopmain.into_container()
    time.sleep(2)  # Добавлено кратковременное ожидание перед созданием контейнера

    container = ShopContainer(chrome_browser)
    container.checkout()
    container.info()
    
    actual_total = container.price()  # Сохраняем результат в переменную

    assert expected_total in actual_total
    print(f"Итоговая сумма равна ${actual_total}")
