# test_main_page.py
import sys
import os
import allure
import pytest
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from pages.main_page import MainPage
from data import TestData
from urls import Urls
from pages.order_page import OrderPage

class TestMainPage:
    # Тесты главной страницы сервиса Самокат.

    @allure.feature('FAQ раздел')
    @allure.title('Проверка ответов на вопросы в FAQ')
    @pytest.mark.parametrize(
        'question_number, expected_text',
        TestData.test_data_question_answer,
        ids=[
            'question_1_about_cost',
            'question_2_about_multiple_scooters',
            'question_3_about_today_order',
            'question_4_about_tomorrow_order',
            'question_5_about_extending_order',
            'question_6_about_charging',
            'question_7_about_cancellation',
            'question_8_about_delivery_radius'
        ]
    )
    def test_faq_question_contains_expected_text(
        self, driver, question_number, expected_text
    ):
        # Проверяет, что ответ на вопрос FAQ содержит ожидаемый текст.
        main_page = MainPage(driver)
        
        # Логируем начало теста
        logger.info(f"Starting FAQ test for question {question_number}")
        
        # Ожидание и прокрутка к FAQ с логированием - ИСПОЛЬЗУЕМ МЕТОДЫ MainPage
        logger.info("Waiting for FAQ section to be visible")
        main_page.wait_for_faq_section_visibility(timeout=15)
        
        logger.info("Scrolling to FAQ section")
        main_page.scroll_to_faq_section()
        
        # Ожидание завершения анимации прокрутки - ИСПОЛЬЗУЕМ МЕТОД BasePage
        main_page.wait_page_loaded(timeout=5)
        
        # Логируем попытку клика на вопрос
        logger.info(f"Clicking on FAQ question {question_number}")
        
        # Проверяем существование вопроса перед кликом - ИСПОЛЬЗУЕМ МЕТОД MainPage
        main_page.wait_for_faq_question_clickable(question_number, timeout=15)
        
        # Основная проверка теста
        assert main_page.verify_faq_answer_contains_text(
            question_number, expected_text
        ), (f'Ответ на вопрос {question_number} не содержит '
            f'ожидаемый текст')
            
        logger.info(f"FAQ test for question {question_number} passed")

    @allure.feature('Навигация')
    @allure.title('Переход на страницу заказа через кнопку в хедере')
    def test_header_order_button_redirects_to_order_page(self, driver):
        # Проверяет переход на страницу заказа через кнопку в хедере.
        main_page = MainPage(driver)
        order_page = OrderPage(driver)

        main_page.click_header_order_button()
        
        assert order_page.is_on_order_page(), (
            'Ожидался переход на страницу заказа'
        )

    @allure.feature('Навигация')
    @allure.title('Переход на страницу заказа через кнопку в основном разделе')
    def test_main_order_button_redirects_to_order_page(self, driver):
        # Проверяет переход на страницу заказа через кнопку в основном разделе.
        main_page = MainPage(driver)
        order_page = OrderPage(driver)
        
        main_page.click_main_order_button()

        assert order_page.is_on_order_page(), (
            'Ожидался переход на страницу заказа'
        )

    @allure.feature('Навигация')
    @allure.title('Редирект на главную страницу при клике на логотип Самоката')
    def test_scooter_logo_redirects_to_main_page(self, driver):
        # Проверяет редирект на главную страницу при клике на логотип Самоката.
        main_page = MainPage(driver)
        
        # Переходим на другую страницу для теста редиректа
        main_page.click_header_order_button()
        
        # Кликаем на логотип и проверяем редирект
        main_page.click_scooter_logo()
        current_url = main_page.get_current_url()
        
        assert main_page.verify_scooter_logo_redirects_to_main_page(), (
            f'Ожидался редирект на главную страницу, текущий URL: {current_url}'
        )

    @allure.feature('Навигация')
    @allure.title('Открытие Дзена в новой вкладке при клике на логотип Яндекса')
    def test_yandex_logo_opens_dzen_in_new_tab(self, driver):
        # Проверяет открытие Дзена в новой вкладке при клике на логотип Яндекса.
        main_page = MainPage(driver)
        
        # Используем метод MainPage вместо прямого вызова
        original_tab = main_page.get_original_tab()
        
        logger.info("Clicking on Yandex logo")
        main_page.wait_for_yandex_logo_clickable(timeout=10)
        main_page.click_yandex_logo()
        
        # Ожидание новой вкладки - ИСПОЛЬЗУЕМ МЕТОД BasePage
        main_page.wait_new_tab_opened(timeout=10)
        
        main_page.switch_to_next_tab()
        
        # Ожидание загрузки новой страницы - ИСПОЛЬЗУЕМ МЕТОД BasePage
        main_page.wait_url_contains(['dzen.ru', 'yandex.ru'], timeout=15)
        
        current_url = main_page.get_current_url()
        assert main_page.is_redirected_to_dzen(), (
            f'Ожидался переход на Дзен, текущий URL: {main_page.get_current_url()}'
        )
        
        logger.info("Yandex logo test passed")
        
        # Используем метод MainPage вместо прямой работы с window handles
        main_page.return_to_original_tab(original_tab)

    @allure.feature('Валидация')
    @allure.title('Проверка отображения основных элементов страницы')
    def test_main_page_elements_are_displayed(self, driver):
        # Проверяет отображение основных элементов главной страницы.
        main_page = MainPage(driver)
    
        assert main_page.is_header_displayed(), 'Главный заголовок не отображается'
    
        assert main_page.is_faq_section_displayed(), 'Раздел FAQ не отображается'
    
        assert main_page.is_header_order_button_displayed(), 'Кнопка заказа в хедере не отображается'

    @allure.feature('Валидация')
    @allure.title('Проверка кликабельности кнопок заказа')
    def test_order_buttons_are_clickable(self, driver):
        # Проверяет, что кнопки заказа кликабельны.
        main_page = MainPage(driver)
        
        assert main_page.is_header_order_button_clickable(), 'Кнопка заказа в хедере не кликабельна'
        
        assert main_page.is_main_order_button_clickable(), 'Кнопка заказа в основном разделе не кликабельна'