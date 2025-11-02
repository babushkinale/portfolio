from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import unittest
import time

class OnlyDigitalFooterTest(unittest.TestCase):
    """
    Автотест для проверки наличия футера, ссылки на Telegram и номера телефона.
    """
    
    TEST_URL = "https://only.digital"
    
    def setUp(self):
        """Настройка: инициализация WebDriver с установкой большого разрешения."""
        self.driver = webdriver.Chrome()
        # Устанавливаем высокое разрешение, чтобы избежать проблем с адаптивным дизайном
        self.driver.set_window_size(1920, 1080) 
        self.driver.implicitly_wait(10) 
        self.driver.get(self.TEST_URL)

    def test_footer_contact_elements(self):
        """Проверка наличия ссылки на Telegram и номера телефона в футере."""
        
        print(f"\nНачинаю проверку страницы: {self.TEST_URL}")

        # 1. Проверка наличия основного элемента футера (<footer>)
        try:
            footer_element = self.driver.find_element(By.TAG_NAME, "footer")
            self.assertTrue(footer_element.is_displayed(), 
                            "❌ Футер (тег <footer>) найден, но не отображается.")
            print("✅ Футер успешно найден и отображается.")
        except NoSuchElementException:
            self.fail("❌ Тест провален: Элемент футера (тег <footer>) не найден на странице.")

        # 2. Проверка элемента: Ссылка на Telegram "@onlydigitalagency"
        try:
            telegram_link = self.driver.find_element(
                By.XPATH, 
                "//footer//a[normalize-space()='@onlydigitalagency']"
            )
            self.assertTrue(telegram_link.is_displayed(), 
                            "❌ Ссылка на Telegram найдена, но не отображается в футере.")
            
            href_attribute = telegram_link.get_attribute("href")
            self.assertIn("t.me", href_attribute, 
                          f"❌ Ссылка на Telegram имеет неверный href: {href_attribute}")
            
            print("✅ Ссылка на Telegram '@onlydigitalagency' найдена и корректна.")
        except NoSuchElementException:
            self.fail("❌ Тест провален: Ссылка на Telegram '@onlydigitalagency' не найдена в футере.")

        # 3. Проверка элемента: Номер телефона
        # Ищем любой элемент внутри футера, содержащий точную последовательность с пробелами
        try:
            phone_number_element = self.driver.find_element(
                By.XPATH, 
                "//footer//*[contains(text(), '062 21 85')]"
            )
            self.assertTrue(phone_number_element.is_displayed(), 
                            "❌ Номер телефона найден, но не отображается в футере.")
            
            print("✅ Номер телефона (по части '062 21 85') найден и отображается.")
        except NoSuchElementException:
            self.fail("❌ Тест провален: Номер телефона ('062 21 85') не найден в футере.")

    def tearDown(self):
        """Очистка: закрытие браузера после каждого теста."""
        self.driver.quit()

if __name__ == '__main__':
    unittest.main(buffer=True)