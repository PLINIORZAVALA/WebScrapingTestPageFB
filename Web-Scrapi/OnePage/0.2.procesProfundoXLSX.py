import sys
import time
import random
import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent
import re

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

def scroll_to_load_more(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)

def close_driver(driver):
    try:
        if driver:
            driver.quit()
    except Exception as e:
        print(f"Error al cerrar el navegador: {e}")

# ---------------------- Función para guardar contenido completo ----------------------

def save_full_page_to_txt(content, file_path, url):
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(f"URL procesada: {url}\n")
            file.write("-" * 50 + "\n")  # Separador
            file.write(content)  # Guardar el código HTML completo de la página
            file.write("\n" + "-" * 50 + "\n")
        print(f"Contenido guardado en: {file_path}")
    except Exception as e:
        print(f"Error al guardar el contenido: {e}")

# ---------------------- Función para crear nombre de archivo seguro ----------------------

def create_safe_filename(url, index):
    # Reemplazar caracteres que no son válidos en nombres de archivos
    safe_url = re.sub(r'[:/\\?=<>|"*]', '_', url)
    # Crear el nombre del archivo con el índice y la URL limpia
    file_name = f"{index+1}_{safe_url}.txt"
    return file_name

# ---------------------- Código Principal ----------------------

def process_urls():
    # Leer el archivo de Excel con las URLs
    df = pd.read_excel('0.1.excelResultProfundo/0.0.urls_extraidas copy.xlsx')

    # Crear el driver
    driver = create_driver()

    # Ruta de salida donde se guardará el archivo de texto
    output_dir = '0.2.salida_txtDelExceldeURLs'  # Cambia esta ruta según tus necesidades
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    try:
        # Recorrer todas las URLs y hacer scraping
        for index, row in df.iterrows():
            url = row['URL']  # Suponiendo que la columna de URLs se llama 'URL'
            print(f"Procesando URL {index+1}/{len(df)}: {url}")

            try:
                # Cargar la página y esperar a que cargue
                load_page(driver, url)

                # Esperar a que se cargue el contenido deseado
                wait_for_element(driver, '//body')  # Esperar a que se cargue el cuerpo de la página

                # Obtener el código HTML completo de la página
                page_source = driver.page_source

                # Crear el nombre del archivo a partir de la URL completa y el índice
                file_name = create_safe_filename(url, index)

                # Ruta completa del archivo de salida
                output_file = os.path.join(output_dir, file_name)

                # Guardar el contenido de la página completa en el archivo correspondiente
                print(f"Guardando contenido de {url} en: {output_file}")
                save_full_page_to_txt(page_source, output_file, url)

                # Desplazarse hacia abajo para cargar más contenido si es necesario
                scroll_to_load_more(driver)

            except Exception as e:
                print(f"Error al procesar {url}: {e}")

    except Exception as e:
        print(f"Ocurrió un error: {e}")
    
    finally:
        # Cerrar el navegador
        close_driver(driver)

# ---------------------- Ejecución ----------------------

if __name__ == "__main__":
    process_urls()
