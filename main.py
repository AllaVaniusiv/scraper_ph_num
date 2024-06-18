import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Налаштування ChromeDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

filename = 'olx_contact_info.csv'

with open(filename, mode='a', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    
    file.seek(0, 2)
    if file.tell() == 0:
        writer.writerow(['Link', 'Contact Info'])

    try:
        url = 'https://www.olx.ua/uk/nedvizhimost/kvartiry/dolgosrochnaya-arenda-kvartir/'

        driver.get(url)

        # Очікування завантаження 3 посилань
        WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a[class="css-z3gu2d"]'))
        )

        # Отримання 3 посилань на оголошення
        links = driver.find_elements(By.CSS_SELECTOR, 'a[class="css-z3gu2d"]')[:3]
        unique_links = [link.get_attribute('href') for link in links]

        for link in unique_links:
            driver.get(link)
            
            # Знаходження кнопки та натискання 
            try:
                button = WebDriverWait(driver, 120).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-cy="ad-contact-phone"]'))
                )
                driver.execute_script("arguments[0].click();", button)

                time.sleep(10) 

                try:
                    contact_info = driver.find_element(By.CSS_SELECTOR, '[data-testid="contact-phone"]').text
                    writer.writerow([link, contact_info])
                except NoSuchElementException:
                    writer.writerow([link, 'Not found'])

            except TimeoutException:
                writer.writerow([link, 'Time out'])

    except TimeoutException:
        print("Time out")

    finally:
        driver.quit()

