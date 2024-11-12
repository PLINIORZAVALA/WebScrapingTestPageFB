import sys
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
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

def scroll_to_bottom(driver):
    """Desplaza la página hacia abajo para cargar todo el contenido."""
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)  # Espera para cargar el contenido nuevo
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def save_page_source(driver, filename='page_source.txt'):
    """Guarda el HTML completo de la página actual en un archivo de texto."""
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(driver.page_source)

# ---------------------- Código Principal ----------------------

def main():
    # URL de la página que queremos extraer
    url = 'https://es.wikipedia.org/wiki/Cifrado_de_extremo_a_extremo'
    
    driver = create_driver()

    try:
        # Carga la página y desplázate para cargar todo el contenido dinámico
        load_page(driver, url)
        scroll_to_bottom(driver)

        # Guarda todo el HTML en un archivo de texto
        save_page_source(driver, 'OnePage/0.0.ScrapeoProfundo.txt')
        print("El HTML de la página completa se ha guardado en 'OnePage/0.0.ScrapeoProfundo.txt'.")
        
    finally:
        # Cierra el navegador
        driver.quit()

if __name__ == "__main__":
    main()
