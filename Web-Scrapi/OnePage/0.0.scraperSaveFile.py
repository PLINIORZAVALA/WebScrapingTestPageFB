import sys
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent
import undetected_chromedriver as uc

# ---------------------- Funciones ----------------------

def create_driver():
    ua = UserAgent()
    user_agent = ua.random

    options = webdriver.ChromeOptions()
    options.add_argument(f'user-agent={user_agent}')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = uc.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def load_page(driver, url):
    driver.get(url)
    time.sleep(random.uniform(2, 5))

def wait_for_element(driver, xpath, timeout=20):
    try:
        WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))
        print("Elemento encontrado.")
    except TimeoutException:
        print("Elemento no encontrado dentro del tiempo esperado.")
        print(driver.page_source)

def get_post_descriptions(driver, xpath, limit=1):
    try:
        post_elements = driver.find_elements(By.XPATH, xpath)
        descriptions = []
        
        for post in post_elements[:limit]:
            time_element = post.find_element(By.XPATH, './/span[contains(@class, "timestampContent")]')
            text_element = post.find_element(By.XPATH, './/div[contains(@class, "userContent")]')
            
            description = {
                'time': time_element.text,
                'text': text_element.text
            }
            descriptions.append(description)
        
        return descriptions
    except NoSuchElementException:
        print(f"No se pudo encontrar el elemento con XPath: {xpath}")
        return []

def scroll_to_load_more(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)

def close_driver(driver):
    try:
        driver.quit()
    except Exception as e:
        print(f"Error al cerrar el navegador: {e}")

# ---------------------- Código Principal ----------------------

def main():
    # Redirigir la salida de consola a un archivo de texto
    with open('consola_output.txt', 'w', encoding='utf-8') as file:
        # Guardar la salida de `print()` en el archivo
        sys.stdout = file

        driver = create_driver()

        try:
            url = 'https://www.todopuebla.com/eventos?ext=html&page=2'
            load_page(driver, url)

            wait_for_element(driver, '//div[contains(@class, "userContent")]')
            post_descriptions = get_post_descriptions(driver, '//div[@class="userContent"]', limit=5)

            if post_descriptions:
                for post in post_descriptions:
                    print(post)
                    print(f"Fecha y hora: {post['time']}")
                    print(f"Texto: {post['text']}\n")
                print("Los datos se han guardado en consola_output.txt correctamente.")
            else:
                print("No se encontraron publicaciones para guardar.")

            scroll_to_load_more(driver)
            more_post_descriptions = get_post_descriptions(driver, '//div[@class="userContent"]', limit=5)

            for post in more_post_descriptions:
                print(post)
                print(f"Fecha y hora: {post['time']}")
                print(f"Texto: {post['text']}\n")

        finally:
            close_driver(driver)

        # Restaurar la salida de consola a su valor predeterminado
        sys.stdout = sys.__stdout__

if __name__ == "__main__":
    main()
