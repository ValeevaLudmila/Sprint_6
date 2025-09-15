from selenium.webdriver.common.by import By

class MainPageLocators:
    main_header = (By.XPATH, '//div[contains(@class, "Home_Header__iJKdX")]')
    faq_section = (By.XPATH, '//div[contains(@class, "Home_FAQ")]')
    
    order_button_in_main = (By.XPATH, "//button[contains(@class, 'Button_Button') and contains(text(), 'Заказать')]")
    order_button_in_header = (By.XPATH, "//button[contains(@class, 'Button_Button__ra12g') and not(contains(@class, 'Button_UltraBig__UU3Lp')) and text()='Заказать']")
    
    order_button_in_header_alt = (By.XPATH, "//div[contains(@class, 'Header_Nav')]//button[text()='Заказать']")
    order_button_in_main_alt = (By.CSS_SELECTOR, "button.Button_Button__ra12g.Button_UltraBig__UU3Lp")
    
    header_logo_scooter = (By.XPATH, "//a[@class='Header_LogoScooter__3lsAR']")
    logo_yandex = (By.XPATH, "//a[@class='Header_LogoYandex__3TSOI']")
    
    faq_questions_items = {
        1: (By.XPATH, "//div[@id='accordion__heading-0' and contains(@class, 'accordion__button')]"),
        2: (By.XPATH, "//div[@id='accordion__heading-1' and contains(@class, 'accordion__button')]"),
        3: (By.XPATH, "//div[@id='accordion__heading-2' and contains(@class, 'accordion__button')]"),
        4: (By.XPATH, "//div[@id='accordion__heading-3' and contains(@class, 'accordion__button')]"),
        5: (By.XPATH, "//div[@id='accordion__heading-4' and contains(@class, 'accordion__button')]"),
        6: (By.XPATH, "//div[@id='accordion__heading-5' and contains(@class, 'accordion__button')]"),
        7: (By.XPATH, "//div[@id='accordion__heading-6' and contains(@class, 'accordion__button')]"),
        8: (By.XPATH, "//div[@id='accordion__heading-7' and contains(@class, 'accordion__button')]")
    }

    faq_answers_items = {
        1: (By.XPATH, "//p[text()='Сутки — 400 рублей. Оплата курьеру — наличными или картой.']"),
        2: (By.XPATH, "//p[text()='Пока что у нас так: один заказ — один самокат. Если хотите покататься с друзьями, можете просто сделать несколько заказов — один за другим.']"),
        3: (By.XPATH, "//p[text()='Допустим, вы оформляете заказ на 8 мая. Мы привозим самокат 8 мая в течение дня. Отсчёт времени аренды начинается с момента, когда вы оплатите заказ курьеру. Если мы привезли самокат 8 мая в 20:30, суточная аренда закончится 9 мая в 20:30.']"),
        4: (By.XPATH, "//p[text()='Только начиная с завтрашнего дня. Но скоро станем расторопнее.']"),
        5: (By.XPATH, "//p[text()='Пока что нет! Но если что-то срочное — всегда можно позвонить в поддержку по красивому номеру 1010.']"),
        6: (By.XPATH, "//p[text()='Самокат приезжает к вам с полной зарядкой. Этого хватает на восемь суток — даже если будете кататься без передышек и во сне. Зарядка не понадобится.']"),
        7: (By.XPATH, "//p[text()='Да, пока самокат не привезли. Штрафа не будет, объяснительной записки тоже не попросим. Все же свои.']"),
        8: (By.XPATH, "//p[text()='Да, обязательно. Всем самокатов! И Москве, и Московской области.']")
    }

    ORDER_BUTTON_IN_HEADER = (By.XPATH, "//button[contains(@class, 'Button_Button__ra12g') and text()='Заказать']")
    ORDER_BUTTON_IN_HEADER_ALT = (By.XPATH, "//div[contains(@class, 'Header_Nav')]//button[text()='Заказать']")
    ANY_ORDER_BUTTON = (By.XPATH, "//button[text()='Заказать']")