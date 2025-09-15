from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import allure
from locators.main_page_locators import MainPageLocators

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.base_url = "https://qa-scooter.praktikum-services.ru/"
    
    def open(self, url_path=""):
        # Открыть страницу
        full_url = self.base_url + url_path
        self.driver.get(full_url)
    
    def wait_for_element(self, locator, timeout=10):
        # Ожидание элемента
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )
    
    def is_element_displayed(self, locator, timeout=10):
        # Проверка отображения элемента
        try:
            element = self.wait_for_element(locator, timeout)
            return element.is_displayed()
        except:
            return False

    @allure.step('Подождать пока элемент загрузится')
    def wait_visibility_of_element(self, locator, timeout=30):
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )
    
    @allure.step('Проверить что элемент отобразился')
    def check_displaying_of_element(self, element):
        return element.is_displayed()
    
    @allure.step('Проверить что элемент по локатору отобразился')
    def check_displaying_of_element_by_locator(self, locator):
        # Проверяет отображение элемента по локатору.
        try:
            element = self.driver.find_element(*locator)
            return element.is_displayed()
        except NoSuchElementException:
            return False
    
    @allure.step('Проверить наличие элемента')
    def is_element_present(self, locator):
        # Проверяет наличие элемента на странице.
        try:
            self.driver.find_element(*locator)
            return True
        except NoSuchElementException:
            return False
    
    @allure.step('Скролл до элемента')
    def scroll_to_element(self, locator):
        element = self.driver.find_element(*locator)
        self.driver.execute_script('arguments[0].scrollIntoView();', element)

    @allure.step('Кликнуть на элемент')
    def click_on_element(self, locator):
        self.driver.find_element(*locator).click()

    @allure.step('Ввести значение "{keys}" в поле ввода')
    def send_keys_to_input(self, locator, keys):
        self.driver.find_element(*locator).send_keys(keys)

    @allure.step('Получить текст на элементе')
    def get_text_to_element(self, locator):
        return self.driver.find_element(*locator).text
    
    @allure.step('Перейти на другую вкладку')
    def switch_to_next_tab(self):
        self.driver.switch_to.window(self.driver.window_handles[1])

    @allure.step('Получить заголовок страницы')
    def get_page_title(self):
        WebDriverWait(self.driver, 6).until(expected_conditions.presence_of_element_located(MainPageLocators.title_dzen))
        return self.driver.title