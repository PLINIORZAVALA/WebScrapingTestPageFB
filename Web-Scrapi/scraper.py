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
    """
    Crea y configura el driver de Selenium con las opciones necesarias,
    incluyendo el user-agent aleatorio y configuración de undetected_chromedriver.
    """
    ua = UserAgent()
    user_agent = ua.random

    options = webdriver.ChromeOptions()
    options.add_argument(f'user-agent={user_agent}')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--headless')  # Puedes eliminarlo si necesitas ver el navegador
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    # Usar undetected-chromedriver
    driver = uc.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def load_page(driver, url):
    """
    Carga la página especificada por la URL.
    """
    driver.get(url)
    # Simula tiempo aleatorio para evitar detección
    time.sleep(random.uniform(2, 5))

def wait_for_element(driver, xpath, timeout=20):
    """
    Espera hasta que el elemento especificado por el XPath esté presente en la página.
    """
    try:
        WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))
        print("Elemento encontrado.")
    except TimeoutException:
        print("Elemento no encontrado dentro del tiempo esperado.")
        print(driver.page_source)  # Imprimir el HTML de la página si no se encuentra el elemento

def get_post_descriptions(driver, xpath, limit=1):
    """
    Obtiene las descripciones de las publicaciones de la página.
    Limita el número de publicaciones a imprimir.
    """
    try:
        post_elements = driver.find_elements(By.XPATH, xpath)
        if post_elements:
            descriptions = [post.text for post in post_elements]
            return descriptions[:limit]  # Retorna solo los primeros 'limit' posts
        else:
            print("No se encontraron publicaciones.")
            return []
    except NoSuchElementException:
        print(f"No se pudo encontrar el elemento con XPath: {xpath}")
        return []

def scroll_to_load_more(driver):
    """
    Desplaza la página hacia abajo para cargar más contenido.
    """
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)  # Espera para que cargue el contenido

def close_driver(driver):
    """
    Cierra el driver de manera segura.
    """
    try:
        driver.quit()
    except Exception as e:
        print(f"Error al cerrar el navegador: {e}")

# ---------------------- Código Principal ----------------------

def main():
    # Crear el driver
    driver = create_driver()

    try:
        # Cargar la página de Facebook
        url = 'https://www.facebook.com/PueblaMillenial'
        load_page(driver, url)

        # Esperar a que el primer elemento de la publicación esté presente
        wait_for_element(driver, '//div[contains(@class, "userContent")]')

        # Obtener las descripciones de las publicaciones (limitado a los primeros 5 posts)
        post_descriptions = get_post_descriptions(driver, '//div[@class="userContent"]', limit=5)

        # Imprimir las descripciones obtenidas
        for description in post_descriptions:
            print(description)

        # Hacer scroll para cargar más contenido
        scroll_to_load_more(driver)

        # Obtener nuevamente las descripciones si se cargó más contenido (limitado a 5 posts)
        post_descriptions = get_post_descriptions(driver, '//div[@class="userContent"]', limit=5)

        # Imprimir las nuevas descripciones
        for description in post_descriptions:
            print(description)

    finally:
        # Cerrar el navegador de manera segura
        close_driver(driver)

if __name__ == "__main__":
    main()
