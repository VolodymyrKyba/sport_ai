from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

# Налаштування Selenium
options = Options()
options.add_argument("--headless")  # Запуск без інтерфейсу
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

# Ініціалізація драйвера
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

try:
    # Відкриваємо Statmuse
    url = "https://www.statmuse.com/"
    driver.get(url)
    time.sleep(3)  # Очікуємо завантаження сайту

    # Знаходимо пошуковий рядок
    search_box = driver.find_element(By.CSS_SELECTOR, 'input.sc-15ql7c7-0')
    search_box.send_keys("Barcelona players assists")  # Запит
    search_box.send_keys(Keys.RETURN)  # Натискаємо Enter

    time.sleep(5)  # Чекаємо завантаження результатів

    # Отримуємо статистику (перша знайдена таблиця)
    players = driver.find_elements(By.CSS_SELECTOR, "div.sc-1caz1xb-0")

    data = []
    for player in players:
        name = player.find_element(By.CSS_SELECTOR, "span.sc-1caz1xb-1").text
        assists = player.find_element(By.CSS_SELECTOR, "span.sc-1caz1xb-2").text
        data.append({"name": name, "assists": assists})

    # Виводимо результат
    print(data)

finally:
    driver.quit()  # Закриваємо браузер

