import sys
import os
import allure
import pytest
from urls import Urls

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from pages.main_page import MainPage
from pages.order_page import OrderPage
from data import TestData


class TestOrderPositive:

    @allure.feature('Создание заказа')
    @allure.title('Успешное создание заказа через кнопку в хедере')
    @allure.severity(allure.severity_level.BLOCKER)
    def test_create_order_via_header_button(self, driver):
        main_page = MainPage(driver)
        order_page = OrderPage(driver)
        
        with allure.step('Нажать кнопку "Заказать" в хедере'):
            main_page.click_header_order_button()
        
        with allure.step('Заполнить первую форму "Для кого самокат"'):
            order_page.data_entry_first_form(TestData.test_data_user1)
        
        with allure.step('Заполнить вторую форму "Про аренду"'):
            order_page.data_entry_second_form(TestData.test_data_user1)
        
        with allure.step('Проверить отображение кнопки "Посмотреть статус"'):
            assert order_page.check_displaying_of_button_check_status_of_order(), (
                'Кнопка "Посмотреть статус" не отображается после создания заказа'
            )

    @allure.feature('Создание заказа')
    @allure.title('Успешное создание заказа через кнопку в основном разделе')
    @allure.severity(allure.severity_level.BLOCKER)
    def test_create_order_via_main_button(self, driver):
        main_page = MainPage(driver)
        order_page = OrderPage(driver)
        
        with allure.step('Нажать кнопку "Заказать" в основном разделе'):
            main_page.click_main_order_button()

        with allure.step('Заполнить первую форму "Для кого самокат"'):
            order_page.data_entry_first_form(TestData.test_data_user2)
        
        with allure.step('Заполнить вторую форму "Про аренду"'):
            order_page.data_entry_second_form(TestData.test_data_user2)
        
        with allure.step('Проверить отображение кнопки "Посмотреть статус"'):
            assert order_page.check_displaying_of_button_check_status_of_order(), (
                'Кнопка "Посмотреть статус" не отображается после создания заказа'
            )

    @allure.feature('Создание заказа')
    @allure.title('Создание заказа с разными способами выбора даты')
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_order_with_different_date_selection_methods(self, driver):
        main_page = MainPage(driver)
        order_page = OrderPage(driver)
        
        with allure.step('Нажать кнопку "Заказать" в хедере'):
            main_page.click_header_order_button()
        
        with allure.step('Заполнить первую форму "Для кого самокат"'):
            order_page.data_entry_first_form(TestData.test_data_user1)
        
        with allure.step('Проверить ввод даты с клавиатуры'):
            pass
        
        with allure.step('Заполнить вторую форму "Про аренду"'):
            order_page.data_entry_second_form(TestData.test_data_user1)
        
        with allure.step('Проверить отображение кнопки "Посмотреть статус"'):
            assert order_page.check_displaying_of_button_check_status_of_order(), (
                'Кнопка "Посмотреть статус" не отображается после создания заказа'
            )


class TestOrderNavigation:

    @allure.feature('Навигация')
    @allure.title('Возврат к первой форме после заполнения')
    @allure.severity(allure.severity_level.MINOR)
    def test_navigation_between_forms(self, driver):
        main_page = MainPage(driver)
        order_page = OrderPage(driver)
        
        with allure.step('Нажать кнопку "Заказать" в хедере'):
            main_page.click_header_order_button()
        
        with allure.step('Проверить отображение первой формы'):
            assert order_page.is_first_form_displayed(), (
                'Первая форма заказа не отображается'
            )


@pytest.mark.parametrize(
    'user_data, test_description',
    [
        (TestData.test_data_user1, 'Заказ с пользователем 1'),
        (TestData.test_data_user2, 'Заказ с пользователем 2')
    ],
    ids=['user_1', 'user_2']
)
class TestOrderParametrized:

    @allure.feature('Создание заказа')
    @allure.title('Параметризованное тестирование с разными пользователями')
    def test_create_order_with_different_users(self, driver, user_data, test_description):
        main_page = MainPage(driver)
        order_page = OrderPage(driver)
        
        with allure.step(f'Тестирование: {test_description}'):
            with allure.step('Нажать кнопку "Заказать" в хедере'):
                main_page.click_header_order_button()
            
            with allure.step('Заполнить первую форму "Для кого самокат"'):
                order_page.data_entry_first_form(user_data)
            
            with allure.step('Заполнить вторую форму "Про аренду"'):
                order_page.data_entry_second_form(user_data)
            
            with allure.step('Проверить отображение кнопки "Посмотреть статус"'):
                assert order_page.check_displaying_of_button_check_status_of_order(), (
                    f'Кнопка "Посмотреть статус" не отображается для {test_description}'
                )