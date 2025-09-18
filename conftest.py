import pytest
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from data import TestData
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@pytest.fixture()
def driver():
    """Фикстура для инициализации и закрытия драйвера."""
    logger.info("Инициализация драйвера Firefox")
    
    try:
        # Явный путь к уже скачанному драйверу
        gecko_path = r'C:\Users\Ludmila\.wdm\drivers\geckodriver\win64\v0.33.0\geckodriver.exe'
        
        # Создаем сервис с явным путем к драйверу
        service = Service(executable_path=gecko_path)
        
        # Инициализируем драйвер с сервисом
        driver = webdriver.Firefox(service=service)
        logger.info("Драйвер успешно инициализирован")
        
        driver.implicitly_wait(10)
        
        logger.info(f"Открытие страницы: {TestData.scooter_address}")
        driver.get(TestData.scooter_address)
        driver.maximize_window()
        
        logger.info("Драйвер готов к использованию")
        yield driver
        
    except Exception as e:
        logger.error(f"Ошибка при инициализации драйвера: {e}")
        raise
    finally:
        logger.info("Завершение работы драйвера")
        if 'driver' in locals() and driver:
            driver.quit()