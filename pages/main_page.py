from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure
from .base_page import BasePage
from locators.main_page_locators import MainPageLocators
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
import logging

logger = logging.getLogger(__name__)

class MainPage(BasePage):
    def __init__(self, driver):
        self.driver = driver
        self.locators = MainPageLocators() 

    def check_element_displayed(self, locator):
        # Проверяет отображение элемента по локатору.
        element = self.wait_visibility_of_element(locator)
        return element.is_displayed()

    def get_current_url(self):
        # Возвращает текущий URL
        return self.driver.current_url
    
    def open_main_page(self):
        # Открыть главную страницу
        self.open()
    
    def click_order_button(self, button_type="main"):
        # Клик по кнопке заказа
        if button_type == "main":
            button = self.wait_for_element(MainPageLocators.order_button_in_main)
        else:
            button = self.wait_for_element(MainPageLocators.order_button_in_header)
        button.click()
    
    def is_faq_section_visible(self):
        # Проверка видимости раздела FAQ
        return self.is_element_displayed(MainPageLocators.faq_section)
    
    def is_header_visible(self):
        # Проверка видимости заголовка
        return self.is_element_displayed(MainPageLocators.main_header)

    @allure.step('Нажать кнопку "Заказать" в хедере')
    def click_header_order_button(self):
        # Кликает на кнопку заказа в хедере.
        try:
            element = self.driver.find_element(*MainPageLocators.order_button_in_header)
            self.driver.execute_script("arguments[0].click();", element)
        except (NoSuchElementException, ElementClickInterceptedException):
            # Просто пробуем альтернативный способ
            element = self.driver.find_element(*MainPageLocators.order_button_in_header_alt)
            self.driver.execute_script("arguments[0].click();", element)

    def click_main_order_button(self):
        # Кликает на кнопку заказа в основном разделе с явным ожиданием.
        try:
            # Ждем, пока кнопка станет кликабельной (до 10 секунд)
            wait = WebDriverWait(self.driver, 10)
            button = wait.until(
                EC.element_to_be_clickable(self.locators.order_button_in_main)
            )
            # Прокручиваем к элементу, если это необходимо
            self.driver.execute_script("arguments[0].scrollIntoView();", button)
            button.click()
            return True
        except TimeoutException:
            # Если основной локатор не сработал, пробуем альтернативные
            alternative_locators = [
                self.locators.order_button_in_main_alt,
                self.locators.ANY_ORDER_BUTTON,
                (By.XPATH, "//button[text()='Заказать']")  # Самый простой локатор
            ]
            for locator in alternative_locators:
                try:
                    buttons = self.driver.find_elements(*locator)
                    for btn in buttons:
                        if btn.is_displayed():
                            self.driver.execute_script("arguments[0].scrollIntoView();", btn)
                            btn.click()
                            return True
                except:
                    continue
            logger.error("Не удалось найти и кликнуть ни одну кнопку 'Заказать' в основном разделе.")
            return False

    @allure.step('Скролл до раздела "Вопросы о важном"')
    def scroll_to_faq_section(self):
        self.scroll_to_element(MainPageLocators.faq_section)

    @allure.step('Нажать на вопрос в FAQ по номеру {question_number}')
    def click_faq_question(self, question_number):
        question_locator = MainPageLocators.faq_questions_items[question_number]
        self.scroll_to_element(question_locator)
        self.click_on_element(question_locator)

    @allure.step('Получить текст ответа на вопрос {question_number}')
    def get_faq_answer_text(self, question_number):
        answer_locator = MainPageLocators.faq_answers_items[question_number]
        self.wait_visibility_of_element(answer_locator)
        return self.get_text_to_element(answer_locator)

    @allure.step('Проверить отображение ответа на вопрос {question_number}')
    def check_faq_answer_displayed(self, question_number):
        answer_locator = MainPageLocators.faq_answers_items[question_number]
        return self.check_displaying_of_element(answer_locator)

    @allure.step('Открыть вопрос №{question_number} и проверить наличие текста "{expected_text}"')
    def verify_faq_answer_contains_text(self, question_number, expected_text):
        self.click_faq_question(question_number)
        answer_text = self.get_faq_answer_text(question_number)
        return expected_text in answer_text

    @allure.step('Проверить переход на главную страницу после клика на логотип Самоката')
    def verify_scooter_logo_redirects_to_main_page(self, expected_url):
        self.click_scooter_logo()
        current_url = self.get_current_url()
        return current_url == expected_url

    @allure.step('Проверить переход на Дзен после клика на логотип Яндекса')
    def verify_yandex_logo_redirects_to_dzen(self):
        self.click_yandex_logo()
        self.switch_to_next_tab()
        current_url = self.get_current_url()
        return 'dzen.ru' in current_url or 'yandex.ru' in current_url
    
    