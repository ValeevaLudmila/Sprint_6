import allure
from .base_page import BasePage
from locators.order_page_locators import OrderPageLocators
from data import TestData
import logging
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from urls import Urls

logger = logging.getLogger(__name__)

class OrderPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.locators = OrderPageLocators()
    
    @allure.step('Открыть страницу заказа')
    def open_order_page(self):
        self.open('/order')

    @allure.step('Проверить, что открыта страница заказа')
    def is_on_order_page(self):
        current_url = self.get_current_url()
        return current_url.startswith(Urls.SCOOTER_ORDER)

    @allure.step('Проверить отображение первой формы заказа')
    def is_first_form_displayed(self):
        try:
            return self.is_element_displayed(self.locators.title_page_personal)
        except NoSuchElementException:
            logger.error("Первая форма заказа не найдена")
            return False
    
    @allure.step('Заполнить персональную информацию')
    def fill_personal_info(self, user_data):
        self.send_keys_to_input(self.locators.name, user_data['name'])
        self.send_keys_to_input(self.locators.lastname, user_data['lastname'])
        self.send_keys_to_input(self.locators.address, user_data['address'])
    
    @allure.step('Нажать кнопку "Далее"')
    def click_next(self):
        self.click_element(self.locators.button_next)

    @allure.step('Заполнение формы "Для кого самокат" и нажатие кнопки "Далее"')
    def data_entry_first_form(self, test_data):
        self.wait_for_element_visibility(self.locators.name)
        self.send_keys_to_input(self.locators.name, test_data[0])
        self.send_keys_to_input(self.locators.lastname, test_data[1])
        self.send_keys_to_input(self.locators.address, test_data[2])
    
        # Работа с метро
        self.click_element(self.locators.metro)
        self.click_element(self.locators.dropdow_list)
    
        self.send_keys_to_input(self.locators.phone, test_data[4])
        self.click_element(self.locators.button_next)

    @allure.step('Заполнение формы "Про аренду"')
    def data_entry_second_form(self, test_data):
        self._fill_rent_form_fields(test_data)
        self._submit_order()
        self._confirm_order()

    @allure.step('Заполнить поля формы аренды')
    def _fill_rent_form_fields(self, test_data):
        self.wait_for_element_visibility(self.locators.date)
        self.send_keys_to_input(self.locators.date, test_data[5])

        self.click_element(self.locators.checkbox_black_color_scooter)

        self.click_element(self.locators.rental_period_dropdown)
        self.click_element(self.locators.rental_period_option)

        self.send_keys_to_input(self.locators.comment, test_data[6])

    @allure.step('Отправить форму заказа')
    def _submit_order(self):
        self.click_element(self.locators.button_make_order)

    @allure.step('Подтвердить заказ')
    def _confirm_order(self):
        try:
            self.click_element(self.locators.button_yes_confirm_order, timeout=5)
            logger.info("Заказ успешно подтвержден")
            
        except TimeoutException:
            logger.warning("Кнопка подтверждения заказа не найдена - возможно заказ уже обработан")
        except (NoSuchElementException, ElementClickInterceptedException) as error:
            logger.warning("Проблема с подтверждением заказа: %s", error)

    @allure.step('Кликнуть по предлагаемому варианту в выпадающем списке станций метро')
    def select_station(self):
        self.click_element(self.locators.dropdow_list)

    @allure.step('Ввести дату заказа "{date}" в инпут "Когда привезти самокат"')
    def send_keys_date_by_keyboard_input(self, date):
        self.send_keys_to_input(self.locators.date, date)

    @allure.step('Кликнуть по выбранной дате в выпадающем календаре')
    def click_date_in_calendar(self):
        try:
            self.click_element(self.locators.calendar_item)
        except (NoSuchElementException, ElementClickInterceptedException) as error:
            logger.error("Не удалось выбрать дату в календаре: %s", error)
            raise

    @allure.step('Проверить что кнопка "Посмотреть статус" отобразилась после создания заказа')
    def check_displaying_of_button_check_status_of_order(self):
        try:
            return self.is_element_displayed(self.locators.button_check_status_of_order)
        except NoSuchElementException:
            logger.error("Кнопка статуса заказа не найдена")
            return False