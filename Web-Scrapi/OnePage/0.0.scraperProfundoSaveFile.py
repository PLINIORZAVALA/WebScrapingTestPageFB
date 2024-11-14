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

# ---------------------- Funciones ----------------------

def create_driver():
    ua = UserAgent()
    user_agent = ua.random

    options = webdriver.ChromeOptions()
    options.add_argument(f'user-agent={user_agent}')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--headless')  # Asegurarse de que el navegador esté en modo headless
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        return driver
    except Exception as e:
        print(f"Error al crear el navegador: {e}")
        sys.exit(1)

def load_page(driver, url):
    driver.get(url)
    time.sleep(random.uniform(2, 5))  # Esperar un poco para que la página cargue

def wait_for_element(driver, xpath, timeout=20):
    try:
        WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))
    except TimeoutException:
        print(f"Elemento no encontrado dentro del tiempo esperado para XPath: {xpath}")
        print(driver.page_source)  # Imprimir el HTML de la página para diagnosticar

def get_post_descriptions(driver, xpath, limit=1):
    descriptions = []
    try:
        post_elements = driver.find_elements(By.XPATH, xpath)
        print(f"Se encontraron {len(post_elements)} elementos con el XPath: {xpath}")  # Imprimir cuántos elementos se encuentran
        for post in post_elements[:limit]:
            try:
                time_element = post.find_element(By.XPATH, './/span[contains(@class, "timestampContent")]')
                text_element = post.find_element(By.XPATH, './/div[contains(@class, "userContent")]')

                description = {
                    'time': time_element.text,
                    'text': text_element.text
                }
                descriptions.append(description)
            except NoSuchElementException:
                pass  # Si no se encuentra el subelemento, lo ignoramos
        
    except NoSuchElementException:
        print(f"No se pudo encontrar el elemento con XPath: {xpath}")
    return descriptions

def scroll_to_load_more(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)

def close_driver(driver):
    try:
        if driver:
            driver.quit()
    except Exception as e:
        print(f"Error al cerrar el navegador: {e}")

# ---------------------- Código Principal ----------------------

def main():
    # Redirigir la salida de consola a un archivo de texto
    with open('0.0.ScrapeoProfundo/0.0.ScrapeoProfundo.txt', 'w', encoding='utf-8') as file:
        # Guardar la salida de `print()` en el archivo
        sys.stdout = file

        driver = create_driver()

        try:
            url = 'https://es.wikipedia.org/wiki/Drosera_indica#:~:text=Esta%20especie%20solo%20se%20reproduce,r%C3%A1pido%20a%20medida%20que%20crecen.'
            load_page(driver, url)

            # Esperar y obtener descripciones de las publicaciones
            wait_for_element(driver, '//div[contains(@class, "userContent")]')
            post_descriptions = get_post_descriptions(driver, '//div[@class="userContent"]', limit=5)

            if post_descriptions:
                for post in post_descriptions:
                    print(f"Fecha y hora: {post['time']}")
                    print(f"Texto: {post['text']}\n")
            else:
                print("No se encontraron publicaciones para guardar.")

            # Desplazarse hacia abajo para cargar más publicaciones
            scroll_to_load_more(driver)
            more_post_descriptions = get_post_descriptions(driver, '//div[@class="userContent"]', limit=5)

            if more_post_descriptions:
                for post in more_post_descriptions:
                    print(f"Fecha y hora: {post['time']}")
                    print(f"Texto: {post['text']}\n")

        except Exception as e:
            print(f"Ocurrió un error: {e}")
        
        finally:
            # Cerrar el navegador
            close_driver(driver)

        # Restaurar la salida de consola a su valor predeterminado
        sys.stdout = sys.__stdout__

if __name__ == "__main__":
    main()
