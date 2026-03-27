# main_page.py
import allure
from .base_page import BasePage
from locators.main_page_locators import MainPageLocators
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
import logging
from urls import Urls

logger = logging.getLogger(__name__)

class MainPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.locators = MainPageLocators()

    @allure.step('Ожидание видимости раздела FAQ')
    def wait_for_faq_section_visibility(self, timeout=10):
        return self.wait_for_element_visibility(self.locators.faq_section, timeout)
    
    @allure.step('Ожидание кликабельности вопроса FAQ {question_number}')
    def wait_for_faq_question_clickable(self, question_number, timeout=10):
        question_locator = self.locators.faq_questions_items[question_number]
        return self.wait_for_element_clickable(question_locator, timeout)
    
    @allure.step('Получить заголовок страницы')
    def get_page_title(self, timeout=10):
        self.wait_for_element_visibility(self.locators.title_dzen, timeout)
        return super().get_page_title()
    
    @allure.step('Ожидание кликабельности логотипа Яндекса')
    def wait_for_yandex_logo_clickable(self, timeout=10):
        return self.wait_for_element_clickable(self.locators.logo_yandex, timeout)
    
    @allure.step('Проверить отображение главного заголовка')
    def is_header_displayed(self):
        return self.is_element_displayed(self.locators.main_header)
    
    @allure.step('Проверить отображение раздела FAQ')
    def is_faq_section_displayed(self):
        return self.is_element_displayed(self.locators.faq_section)
    
    @allure.step('Проверить отображение кнопки заказа в хедере')
    def is_header_order_button_displayed(self):
        return self.is_element_displayed(self.locators.order_button_in_header)
 
    @allure.step('Открыть главную страницу')
    def open_main_page(self):
        self.open()
    
    @allure.step('Нажать кнопку заказа')
    def click_order_button(self, button_type="main"):
        if button_type == "main":
            locator = self.locators.order_button_in_main
        else:
            locator = self.locators.order_button_in_header
        self.click_element(locator)
    
    @allure.step('Проверить видимость раздела FAQ')
    def is_faq_section_visible(self):
        return self.is_element_displayed(self.locators.faq_section)
    
    @allure.step('Проверить видимость заголовка')
    def is_header_visible(self):
        return self.is_element_displayed(self.locators.main_header)

    @allure.step('Нажать кнопку "Заказать" в хедере')
    def click_header_order_button(self):
        try:
            self.click_element(self.locators.order_button_in_header)
        except (NoSuchElementException, ElementClickInterceptedException):
            self.click_element(self.locators.order_button_in_header_alt)

    @allure.step('Нажать кнопку "Заказать" в основном разделе') 
    def click_main_order_button(self):
        try:
            self.scroll_to_element(self.locators.order_button_in_main)
            self.click_element(self.locators.order_button_in_main)
            return True
        
        except TimeoutException:
            alternative_locators = [
                self.locators.order_button_in_main_alt,
                self.locators.ANY_ORDER_BUTTON
            ]
            
            for locator in alternative_locators:
                try:
                    self.scroll_to_element(locator)
                    self.click_element(locator)
                    return True
                except (NoSuchElementException, TimeoutException, ElementClickInterceptedException):
                    continue
            logger.error("Не удалось найти и кликнуть ни одну кнопку 'Заказать' в основном разделе.")
            return False

    @allure.step('Скролл до раздела "Вопросы о важном"')
    def scroll_to_faq_section(self):
        self.scroll_to_element(self.locators.faq_section)

    @allure.step('Нажать на вопрос в FAQ по номеру {question_number}')
    def click_faq_question(self, question_number):
        question_locator = self.locators.faq_questions_items[question_number]
        self.scroll_to_element(question_locator)
        self.click_element(question_locator)

    @allure.step('Получить текст ответа на вопрос {question_number}')
    def get_faq_answer_text(self, question_number):
        answer_locator = self.locators.faq_answers_items[question_number]
        self.wait_for_element_visibility(answer_locator)
        return self.get_element_text(answer_locator)

    @allure.step('Проверить отображение ответа на вопрос {question_number}')
    def check_faq_answer_displayed(self, question_number):
        answer_locator = self.locators.faq_answers_items[question_number]
        return self.is_element_displayed(answer_locator)

    @allure.step('Открыть вопрос №{question_number} и проверить наличие текста "{expected_text}"')
    def verify_faq_answer_contains_text(self, question_number, expected_text):
        self.click_faq_question(question_number)
        answer_text = self.get_faq_answer_text(question_number)
        return expected_text in answer_text

    @allure.step('Кликнуть на логотип Самоката')
    def click_scooter_logo(self):
        self.click_element(self.locators.header_logo_scooter)

    @allure.step('Кликнуть на логотип Яндекса')
    def click_yandex_logo(self):
        self.click_element(self.locators.logo_yandex)

    @allure.step('Проверить переход на главную страницу после клика на логотип Самоката')
    def verify_scooter_logo_redirects_to_main_page(self):
        self.click_scooter_logo()
        return self.is_url_equal(Urls.SCOOTER_MAIN, timeout=10)

    @allure.step('Проверить переход на Дзен после клика на логотип Яндекса')
    def verify_yandex_logo_redirects_to_dzen(self):
        self.click_yandex_logo()
        self.wait_new_tab_opened()
        self.switch_to_next_tab()
        self.wait_url_contains([Urls.YANDEX_DZEN, Urls.YANDEX_MAIN], timeout=15)
        return self.is_redirected_to_dzen()
    
    @allure.step('Получить handle текущей вкладки')
    def get_original_tab(self):
        return self.get_current_window_handle()

    @allure.step('Вернуться к исходной вкладке {original_tab} и закрыть текущую')
    def return_to_original_tab(self, original_tab):
        self.close_current_tab()
        self.switch_to_window(original_tab)

    @allure.step('Проверить кликабельность кнопки заказа в хедере')
    def is_header_order_button_clickable(self, timeout=10):
        try:
            return self.wait_for_element_clickable(self.locators.order_button_in_header, timeout)
        except TimeoutException:
            # Попробуем альтернативный локатор, если основной не найден
            try:
                return self.wait_for_element_clickable(self.locators.order_button_in_header_alt, timeout)
            except TimeoutException:
                return False

    @allure.step('Проверить кликабельность кнопки заказа в основном разделе')
    def is_main_order_button_clickable(self, timeout=10):
        try:
            return self.wait_for_element_clickable(self.locators.order_button_in_main, timeout)
        except TimeoutException:
            # Попробуем альтернативные локаторы, если основной не найден
            alternative_locators = [
                self.locators.order_button_in_main_alt,
                self.locators.ANY_ORDER_BUTTON
            ]
            
            for locator in alternative_locators:
                try:
                    if self.wait_for_element_clickable(locator, timeout=1):
                        return True
                except TimeoutException:
                    continue
            return False 

    @allure.step('Проверить переход на Дзен')
    def is_redirected_to_dzen(self):
        """Проверяет, что произошел переход на Дзен или Яндекс"""
        return self.is_url_contains(Urls.YANDEX_DZEN) or self.is_url_contains(Urls.YANDEX_MAIN)