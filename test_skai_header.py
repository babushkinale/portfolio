from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import unittest
from typing import List, Tuple

class SkaiHeaderTest(unittest.TestCase):
    """
    Автотест для проверки наличия хедера, логотипа (как первой ссылки) 
    и всех ключевых элементов навигационного меню на сайте https://skai.online/.
    """
    
    TEST_URL = "https://skai.online/"
    
    # Список ожидаемых текстовых ссылок в меню
    EXPECTED_MENU_LINKS: List[str] = [
        "О компании", 
        "Решения", 
        "Новости", 
        "Отрасли", 
        "IT услуги", 
        "Комплаенс", 
        "Карьера", 
        "Контакты"
    ]

    # Список ожидаемых текстовых кнопок
    EXPECTED_BUTTONS: List[str] = [
        "Демо-доступ",
        "Оставить заявку"
    ]
    
    def setUp(self):
        """Настройка: инициализация WebDriver и установка разрешения."""
        self.driver = webdriver.Chrome() 
        self.driver.set_window_size(1920, 1080) 
        self.driver.implicitly_wait(10) 
        self.driver.get(self.TEST_URL)

    def test_header_elements_presence(self):
        """Проверка наличия хедера, логотипа (ссылки), ссылок и кнопок."""
        
        print(f"\nНачинаю проверку хедера страницы: {self.TEST_URL}")

        # 1. Проверка наличия основного элемента хедера 
        HEADER_LOCATOR: Tuple[By, str] = (By.TAG_NAME, "header")
        try:
            header_element = self.driver.find_element(*HEADER_LOCATOR)
            self.assertTrue(header_element.is_displayed(), 
                            "❌ Хедер (тег <header>) найден, но не отображается.")
            print("✅ Хедер успешно найден и отображается.")
        except NoSuchElementException:
            self.fail("❌ Тест провален: Элемент хедера не найден на странице.")
            
        # 2. Проверка наличия логотипа (как первой ссылки <a> в хедере)
        # Это универсальный локатор, который должен найти логотип, независимо от его класса или текста.
        LOGO_LOCATOR: str = "//header//a[1]" 
        try:
            logo_element = self.driver.find_element(By.XPATH, LOGO_LOCATOR)
            self.assertTrue(logo_element.is_displayed(), 
                            "❌ Логотип (первая ссылка в хедере) найден, но не отображается.")
            print("✅ Логотип (первая ссылка в хедере) успешно найден.")
        except NoSuchElementException:
            self.fail("❌ Тест провален: Логотип (первая ссылка <a>) не найден в хедере.")

        # 3. Проверка наличия всех ссылок меню
        print("\nПроверка ссылок меню:")
        for link_text in self.EXPECTED_MENU_LINKS:
            link_locator: str = f"//header//a[normalize-space()='{link_text}']"
            try:
                link_element = self.driver.find_element(By.XPATH, link_locator)
                self.assertTrue(link_element.is_displayed(), f"❌ Ссылка '{link_text}' найдена, но не отображается.")
                print(f"  ✅ Ссылка '{link_text}' найдена.")
            except NoSuchElementException:
                self.fail(f"❌ Тест провален: Ссылка '{link_text}' не найдена в хедере.")

        # 4. Проверка наличия кнопок
        print("\nПроверка кнопок:")
        for button_text in self.EXPECTED_BUTTONS:
            button_locator: str = f"//header//*[normalize-space()='{button_text}']"
            try:
                button_element = self.driver.find_element(By.XPATH, button_locator)
                self.assertTrue(button_element.is_displayed(), f"❌ Кнопка '{button_text}' найдена, но не отображается.")
                print(f"  ✅ Кнопка '{button_text}' найдена.")
            except NoSuchElementException:
                self.fail(f"❌ Тест провален: Кнопка '{button_text}' не найдена в хедере.")

    def tearDown(self):
        """Очистка: закрытие браузера после каждого теста."""
        self.driver.quit()

if __name__ == '__main__':
    unittest.main(buffer=True)