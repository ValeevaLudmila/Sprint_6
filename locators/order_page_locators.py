from selenium.webdriver.common.by import By

class OrderPageLocators:
    # Первая страница
    title_page_personal = (By.XPATH, "//div[text()='Для кого самокат']")
    name = (By.XPATH, "//input[@placeholder='* Имя']")
    lastname = (By.XPATH, "//input[@placeholder='* Фамилия']")
    address = (By.XPATH, "//input[@placeholder='* Адрес: куда привезти заказ']")
    metro = (By.XPATH, "//input[@placeholder='* Станция метро']")
    phone = (By.XPATH, "//input[@placeholder='* Телефон: на него позвонит курьер']")
    button_next = (By.XPATH, "//button[text()='Далее']")
    dropdow_list = (By.CLASS_NAME, "select-search__row")
    
    # Вторая страница
    title_page_rent = (By.XPATH, "//div[text()='Про аренду']")
    date = (By.XPATH, "//input[@placeholder='* Когда привезти самокат']")
    checkbox_black_color_scooter = (By.ID, "black")
    rental_period_dropdown = (By.XPATH, "//div[text()='* Срок аренды']")
    rental_period_option = (By.XPATH, "//div[text()='сутки']")  # Добавлен недостающий локатор
    comment = (By.XPATH, "//input[@placeholder='Комментарий для курьера']")
    button_make_order = (By.XPATH, "//button[contains(@class, 'Button_Button__ra12g') and contains(@class, 'Button_Middle__1CSJM') and text()='Заказать']")
    
    # Подтверждение заказа
    button_yes_confirm_order = (By.XPATH, "//button[text()='Да']")
    button_check_status_of_order = (By.XPATH, "//button[contains(@class, 'Button_Button__ra12g') and contains(@class, 'Button_Middle__1CSJM') and text()='Посмотреть статус']")
    status_order_button_partial_class = (By.XPATH, "//button[contains(@class, 'Header_Link') and text()='Статус заказа']")
    