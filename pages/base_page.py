from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import allure
from urls import Urls
import logging

logger = logging.getLogger(__name__)

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.base_url = Urls.SCOOTER_MAIN
        self.wait = WebDriverWait(self.driver, 10)
    
    def _get_driver(self):
        """Внутренний метод для доступа к драйверу """
        return self.driver
   
    @allure.step('Ожидание выполнения условия')
    def wait_until(self, condition, timeout=10, message=""):
        return self.wait.until(condition, message=message)
    
    @allure.step('Открыть страницу "{url_path}"')
    def open(self, url_path=""):
        full_url = self.base_url + url_path
        self.driver.get(full_url)
    
    @allure.step('Получить текущий URL')
    def get_current_url(self):
        return self.driver.current_url
    
    @allure.step('Получить заголовок страницы')
    def get_page_title(self):
        return self.driver.title

    @allure.step('Получить текущий window handle')
    def get_current_window_handle(self):
        return self.driver.current_window_handle
    
    @allure.step('Закрыть текущую вкладку')
    def close_current_tab(self):
        self.driver.close()
    
    @allure.step('Переключиться на окно по handle')
    def switch_to_window(self, window_handle):
        self.driver.switch_to.window(window_handle)
    
    @allure.step('Ожидание видимости элемента')
    def wait_for_element_visibility(self, locator, timeout=10):
        return self.wait_until(EC.visibility_of_element_located(locator), timeout)
    
    @allure.step('Ожидание присутствия элемента в DOM')
    def wait_for_element_presence(self, locator, timeout=10):
        return self.wait_until(EC.presence_of_element_located(locator), timeout)
    
    @allure.step('Ожидание кликабельности элемента')
    def wait_for_element_clickable(self, locator, timeout=10):
        return self.wait_until(EC.element_to_be_clickable(locator), timeout)
     
    @allure.step('Ожидание исчезновения элемента')
    def wait_for_element_invisibility(self, locator, timeout=10):
        return self.wait_until(EC.invisibility_of_element_located(locator), timeout)
    
    @allure.step('Ожидание появления текста в элементе')
    def wait_for_text_in_element(self, locator, text, timeout=10):
        return self.wait_until(EC.text_to_be_present_in_element(locator, text), timeout)
    
    @allure.step('Проверить отображение элемента')
    def is_element_displayed(self, locator, timeout=10):
        try:
            element = self.wait_for_element_visibility(locator, timeout)
            return element.is_displayed()
        except (NoSuchElementException, TimeoutException):
            return False
    
    @allure.step('Проверить наличие элемента')
    def is_element_present(self, locator, timeout=10):
        try:
            self.wait_for_element_presence(locator, timeout)
            return True
        except (NoSuchElementException, TimeoutException):
            return False
    
    @allure.step('Кликнуть на элемент')
    def click_element(self, locator, timeout=10):
        element = self.wait_for_element_clickable(locator, timeout)
        element.click()
    
    @allure.step('Ввести значение "{keys}" в поле ввода')
    def send_keys_to_input(self, locator, keys, timeout=10):
        element = self.wait_for_element_clickable(locator, timeout)
        element.click() 
        element.clear()
        element.send_keys(keys)
    
    @allure.step('Получить текст элемента')
    def get_element_text(self, locator, timeout=10):
        element = self.wait_for_element_visibility(locator, timeout)
        return element.text
    
    @allure.step('Выполнить JavaScript скрипт: {script}')
    def execute_script_safe(self, script, *args, timeout=10):
        """Безопасное выполнение JavaScript скрипта с ожиданием"""
        try:
            self.wait_until(
                lambda driver: driver.execute_script(script, *args) or True,
                timeout
            )
        except Exception as e:
            logger.warning(f"Ошибка при выполнении скрипта: {e}")
            self.driver.execute_script(script, *args)

    @allure.step('Скролл до элемента')
    def scroll_to_element(self, locator, timeout=10):
        element = self.wait_for_element_presence(locator, timeout)
        self.execute_script_safe('arguments[0].scrollIntoView();', element)
    
    @allure.step('Найти элемент по локатору')
    def find_element(self, locator, timeout=10):
        return self.wait_for_element_presence(locator, timeout)
    
    @allure.step('Найти все элементы по локатору')
    def find_elements(self, locator, timeout=10):
        try:
            return self.wait_until(EC.presence_of_all_elements_located(locator), timeout)
        except TimeoutException:
            return []
    
    @allure.step('Выполнить JavaScript: {script}')
    def execute_script(self, script, *args):
        return self.driver.execute_script(script, *args)
    
    @allure.step('Переключиться на окно по индексу {index}')
    def switch_to_window_by_index(self, index, timeout=10):
        """Безопасное переключение на окно по индексу с ожиданием"""
        try:
            self.wait_until(
                lambda driver: len(self.get_window_handles()) > index,
                timeout,
                f"Не дождались открытия окна с индексом {index}"
            )

            window_handle = self.get_window_handles()[index]
            self.switch_to_window_direct(window_handle)
            self.wait_page_loaded(timeout)
            return True
    
        except (TimeoutException, IndexError):
            logger.warning(f"Не удалось переключиться на окно с индексом {index}")
            return False
    
    @allure.step('Перейти на другую вкладку')
    def switch_to_next_tab(self, timeout=10):
        return self.switch_to_window_by_index(1, timeout)
    
    @allure.step('Ожидание загрузки страницы')
    def wait_page_loaded(self, timeout=10):
        return self.wait_until(
            lambda d: d.execute_script("return document.readyState") == 'complete',
            timeout,
            "Страница не загрузилась в течение заданного времени"
        )
    
    @allure.step('Ожидание новой вкладки')
    def wait_new_tab_opened(self, timeout=10):
        return self.wait_until(
            lambda d: len(d.window_handles) > 1,
            timeout,
            "Новая вкладка не открылась в течение заданного времени"
        )
    
    @allure.step('Ожидание URL содержащего {domains}')
    def wait_url_contains(self, domains, timeout=10):
        return self.wait_until(
            lambda d: any(domain in d.current_url for domain in domains),
            timeout,
            f"URL не содержит ожидаемых доменов: {domains}"
        )
    
    @allure.step('Получить handles всех окон')
    def get_window_handles(self):
        return self.driver.window_handles

    @allure.step('Проверить, что URL содержит {expected_url}')
    def is_url_contains(self, expected_url, timeout=10):
        """Проверяет, что текущий URL содержит ожидаемую строку"""
        try:
            return self.wait_until(
                lambda d: expected_url in d.current_url,
                timeout,
                f"URL не содержит '{expected_url}' в течение {timeout} секунд"
            )
        except TimeoutException:
            return False

    @allure.step('Проверить, что URL равен {expected_url}')
    def is_url_equal(self, expected_url, timeout=10):
        """Проверяет, что текущий URL точно равен ожидаемому"""
        try:
            return self.wait_until(
                lambda d: d.current_url == expected_url,
                timeout,
                f"URL не равен '{expected_url}' в течение {timeout} секунд"
            )
        except TimeoutException:
            return False

    @allure.step('Ожидание URL содержащего {domains}')
    def wait_url_contains(self, domains, timeout=10):
        return self.wait_until(
            lambda d: any(domain in d.current_url for domain in domains),
            timeout,
            f"URL не содержит ожидаемых доменов: {domains}"
        )

    @allure.step('Переключиться на frame по локатору')
    def switch_to_frame(self, locator, timeout=10):
        """Переключиться на frame по локатору"""
        frame_element = self.wait_for_element_presence(locator, timeout)
        self.driver.switch_to.frame(frame_element)

    @allure.step('Переключиться на основной контент')
    def switch_to_default_content(self):
        """Переключиться на основной контент страницы"""
        self.driver.switch_to.default_content()

    @allure.step('Переключиться на alert')
    def switch_to_alert(self, timeout=10):
        """Переключиться на alert и вернуть его объект"""
        return self.wait_until(EC.alert_is_present(), timeout, "Alert не появился")

    @allure.step('Принять alert')
    def accept_alert(self, timeout=10):
        """Принять alert"""
        alert = self.switch_to_alert(timeout)
        alert.accept()

    @allure.step('Отклонить alert')
    def dismiss_alert(self, timeout=10):
        """Отклонить alert"""
        alert = self.switch_to_alert(timeout)
        alert.dismiss()

    @allure.step('Переключиться на окно по handle')
    def switch_to_window_direct(self, window_handle):
        """Прямое переключение на окно по handle"""
        self.driver.switch_to.window(window_handle)