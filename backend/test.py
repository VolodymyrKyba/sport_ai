from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

def get_current_head_coach(team_name):
    options = Options()
    options.add_argument("--headless")  # Прихований режим
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

    try:
        query = f"{team_name} current head coach"
        url = f"https://www.google.com/search?q={query}"
        driver.get(url)
        time.sleep(2)  # Даємо сторінці завантажитись

        # Шукаємо перший блок результату
        results = driver.find_elements(By.CSS_SELECTOR, "h3")
        if results:
            coach_name = results[0].text
        else:
            coach_name = "Coach not found"

        print(f"Current Head Coach of {team_name}: {coach_name}")
        return coach_name

    finally:
        driver.quit()
get_current_head_coach("Liverpool")
get_current_head_coach("Real Madrid")
get_current_head_coach("Manchester City")
