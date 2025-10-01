import pytest
import os
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from urls import Urls
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_driver_service():
    gecko_path = os.getenv('GECKODRIVER_PATH')
    
    if gecko_path and os.path.exists(gecko_path):
        logger.info(f"Используется драйвер из GECKODRIVER_PATH: {gecko_path}")
        return Service(executable_path=gecko_path)
    else:
        if gecko_path:
            logger.warning(f"Указанный GECKODRIVER_PATH не существует: {gecko_path}")
        logger.info("Используется драйвер из системного PATH")
        return Service()

@pytest.fixture()
def driver():
    logger.info("Инициализация драйвера Firefox")
    
    driver = None
    try:
        service = get_driver_service()
        driver = webdriver.Firefox(service=service)
        
        logger.info("Драйвер успешно инициализирован")
        
        driver.implicitly_wait(10)
        driver.get(Urls.SCOOTER_MAIN)
        driver.maximize_window()
        
        logger.info("Драйвер готов к использованию")
        yield driver
        
    except Exception as e:
        logger.error(f"Ошибка при инициализации драйвера: {e}")
        raise
    finally:
        logger.info("Завершение работы драйвера")
        if driver:
            driver.quit()