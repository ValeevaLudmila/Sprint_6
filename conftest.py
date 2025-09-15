import pytest
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
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
        service = Service(GeckoDriverManager(version="v0.33.0").install())
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
        driver.quit()