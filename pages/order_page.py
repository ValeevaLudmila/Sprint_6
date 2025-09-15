from selenium.webdriver.common.by import By
import allure
from .base_page import BasePage
from locators.order_page_locators import OrderPageLocators
from data import TestData
import logging
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException

logger = logging.getLogger(__name__)


class OrderPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
    
    def open_order_page(self):
        # Открыть страницу заказа
        self.open("order")
    
    def fill_personal_info(self, user_data):
        # Заполнение персональной информации
        self.wait_for_element(OrderPageLocators.name).send_keys(user_data['name'])
        self.wait_for_element(OrderPageLocators.lastname).send_keys(user_data['lastname'])
        self.wait_for_element(OrderPageLocators.address).send_keys(user_data['address'])
        # ... остальные поля
    
    def click_next(self):
        # Клик на кнопку Далее
        self.wait_for_element(OrderPageLocators.button_next).click()

    @allure.step('Заполнение формы "Для кого самокат" и нажатие кнопки "Далее"')
    def data_entry_first_form(self, test_data):
        # Заполняет первую форму заказа с данными пользователя.
        self.wait_visibility_of_element(OrderPageLocators.name)
        self.send_keys_to_input(OrderPageLocators.name, test_data[0])
        self.send_keys_to_input(OrderPageLocators.lastname, test_data[1])
        self.send_keys_to_input(OrderPageLocators.address, test_data[2])
    
        # Работа с метро
        self.click_on_element(OrderPageLocators.metro)
        dropdown_option = self.wait_visibility_of_element(OrderPageLocators.dropdow_list)
        dropdown_option.click()
    
        self.send_keys_to_input(OrderPageLocators.phone, test_data[4])
        self.click_on_element(OrderPageLocators.button_next)

    @allure.step('Заполнение формы "Про аренду"')
    def data_entry_second_form(self, test_data):
        # Заполняет вторую форму заказа с данными аренды.
        self._fill_rent_form_fields(test_data)
        self._submit_order()
        self._confirm_order()

    def _fill_rent_form_fields(self, test_data):
        # Заполняет поля формы аренды.
        self.wait_visibility_of_element(OrderPageLocators.date)
        self.send_keys_to_input(OrderPageLocators.date, test_data[5])

        self.click_on_element(OrderPageLocators.checkbox_black_color_scooter)

        self.click_on_element(OrderPageLocators.rental_period_dropdown)
        self.click_on_element(OrderPageLocators.rental_period_option)

        self.send_keys_to_input(OrderPageLocators.comment, test_data[6])

    def _submit_order(self):
        # Отправляет форму заказа.
        self.click_on_element(OrderPageLocators.button_make_order)

    def _confirm_order(self):
        # Подтверждает заказ, обрабатывая возможные сценарии.
        try:
            self.wait_visibility_of_element(OrderPageLocators.button_yes_confirm_order, timeout=5)
            self.click_on_element(OrderPageLocators.button_yes_confirm_order)
            logger.info("Заказ успешно подтвержден")
            
        except TimeoutException:
            logger.warning("Кнопка подтверждения заказа не найдена - возможно заказ уже обработан")
            # Продолжаем выполнение, так как это не критическая ошибка
            
        except (NoSuchElementException, ElementClickInterceptedException) as error:
            logger.warning("Проблема с подтверждением заказа: %s", error)
            # Продолжаем выполнение, так как это не критическая ошибка

    @allure.step('Кликнуть по предлагаемому варианту в выпадающем списке станций метро')
    def select_station(self):
        # Выбирает станцию метро из выпадающего списка.
        self.click_on_element(OrderPageLocators.dropdow_list)

    @allure.step('Ввести дату заказа в инпут "Когда привезти самокат"')
    def send_keys_date_by_keyboard_input(self):
        # Вводит дату заказа с клавиатуры.
        date_input = self.driver.find_element(*OrderPageLocators.date)
        date_input.send_keys(TestData.test_data_user1[5])

    @allure.step('Кликнуть по выбранной дате в выпадающем календаре')
    def click_date_in_calendar(self):
        # Выбирает дату в календаре.
        try:
            self.click_on_element(OrderPageLocators.calendar_item)
        except (NoSuchElementException, ElementClickInterceptedException) as error:
            logger.error("Не удалось выбрать дату в календаре: %s", error)
            raise

    @allure.step('Проверить что кнопка "Посмотреть статус" отобразилась после создания заказа')
    def check_displaying_of_button_check_status_of_order(self):
        # Проверяет отображение кнопки статуса заказа.
        try:
            return self.check_displaying_of_element_by_locator(OrderPageLocators.button_check_status_of_order)
        except NoSuchElementException:
            logger.error("Кнопка статуса заказа не найдена")
            return False