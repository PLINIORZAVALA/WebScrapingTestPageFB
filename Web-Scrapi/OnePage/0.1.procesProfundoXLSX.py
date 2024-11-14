import time
import random
import pandas as pd
import sys
import os
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
    time.sleep(random.uniform(2, 5))  # Espera para cargar la página

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

def save_page_source(driver, url, index):
    """Guarda el HTML completo de la página actual en un archivo de texto con un nombre basado en la URL."""
    file_name = f"resultAllPagesExcel/{index+1}_{url.replace('https://', '').replace('www.', '').replace('/', '_')}.txt"
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(driver.page_source)
    print(f"Se ha guardado el contenido de {url} en {file_name}")

# ---------------------- Código Principal ----------------------

def process_urls():
    # Leer el archivo de Excel con las URLs
    df = pd.read_excel('excelResultProfundo/0.0.urls_extraidas.xlsx')

    # Crear carpeta para guardar los archivos si no existe
    if not os.path.exists('resultAllPagesExcel'):
        os.makedirs('resultAllPagesExcel')

    # Crear el driver
    driver = create_driver()

    try:
        # Recorrer todas las URLs y hacer scraping
        for index, row in df.iterrows():
            url = row['URL']  # Suponiendo que la columna de URLs se llama 'URL'
            print(f"Procesando URL {index+1}/{len(df)}: {url}")

            try:
                # Cargar la página y desplazarse hacia abajo
                load_page(driver, url)
                scroll_to_bottom(driver)

                # Guardar el contenido de la página
                save_page_source(driver, url, index)

            except Exception as e:
                print(f"Error al procesar {url}: {e}")
                continue  # Si no se puede procesar la URL, pasa a la siguiente

    finally:
        driver.quit()  # Cerrar el navegador

# ---------------------- Ejecución ----------------------

if __name__ == "__main__":
    process_urls()
