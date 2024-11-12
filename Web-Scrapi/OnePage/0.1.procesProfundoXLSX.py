import os
import time
import random
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent
import undetected_chromedriver as uc
import re  # Para reemplazar caracteres no válidos en nombres de archivos

# ---------------------- Funciones ----------------------

def create_driver():
    """Crea el driver con un User-Agent aleatorio y configuración sin cabeza (headless)."""
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
    """Carga la página especificada en la URL."""
    driver.get(url)
    time.sleep(random.uniform(2, 5))  # Espera aleatoria para simular comportamiento humano

def scroll_to_bottom(driver):
    """Desplaza la página hacia abajo para cargar todo el contenido dinámico."""
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)  # Espera para cargar el contenido nuevo
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def save_page_source(driver, filename):
    """Guarda el HTML completo de la página actual en un archivo de texto."""
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(driver.page_source)

# ---------------------- Función para leer URLs desde Excel ----------------------

def scrape_urls_from_excel(input_excel, output_folder):
    """Lee las URLs desde un archivo Excel y procesa cada URL guardando su contenido en archivos .txt."""
    # Cargar el archivo Excel con pandas
    df = pd.read_excel(input_excel)

    # Asegúrate de que la columna con URLs se llama 'URL', si tiene otro nombre ajusta este campo
    urls = df['URL'].dropna().tolist()

    # Crear un directorio de salida si no existe
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Crear el driver de Selenium
    driver = create_driver()

    # Iterar sobre cada URL en el archivo Excel
    for idx, url in enumerate(urls, start=1):  # Añadimos un índice que comienza desde 1
        print(f"Procesando URL: {url}")
        try:
            # Cargar la página y desplazarse hacia abajo para cargar contenido dinámico
            load_page(driver, url)
            scroll_to_bottom(driver)

            # Formatear la URL para usarla como nombre de archivo (reemplazar caracteres no válidos)
            valid_filename = re.sub(r'[\\/*?:"<>|]', '_', url)  # Reemplaza caracteres no válidos con '_'
            filename = f"{output_folder}/{idx}_{valid_filename}.txt"  # Añadimos la enumeración al nombre del archivo
            
            # Guardar el HTML de la página en un archivo de texto
            save_page_source(driver, filename)
            print(f"El HTML de la página {url} se ha guardado en '{filename}'.")

        except Exception as e:
            print(f"Error procesando la URL {url}: {e}")

    # Cerrar el driver después de procesar todas las URLs
    driver.quit()

# ---------------------- Código Principal ----------------------

def main():
    # Definir la ruta del archivo Excel y la carpeta de salida
    input_excel = 'excelResultProfundo/0.0.urls_extraidas.xlsx'  # Ajusta esta ruta si es necesario
    output_folder = 'resultAllPagesExcel'

    # Ejecutar la función de scraping
    scrape_urls_from_excel(input_excel, output_folder)

    print(f"El contenido de todas las páginas se ha guardado en '{output_folder}'.")

if __name__ == "__main__":
    main()
