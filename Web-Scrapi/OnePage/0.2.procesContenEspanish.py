import os
import pandas as pd
from langdetect import detect
import re

# Ruta de la carpeta con los archivos HTML
input_folder = 'resultAllPagesExcel'
output_excel = 'filtered_urls_with_languages.xlsx'

def extract_text_from_html(file_path):
    """Extrae texto del contenido del archivo HTML."""
    text = ""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
            # Extraer el contenido eliminando etiquetas HTML
            text = re.sub('<[^<]+?>', '', html_content)
    except Exception as e:
        print(f"Error al leer {file_path}: {e}")
    return text

def detect_language_content(text):
    """Detecta si el texto está en español o inglés usando langdetect."""
    try:
        # Detecta el idioma principal del contenido
        lang = detect(text)
        if lang == 'es':
            return 'español'
        elif lang == 'en':
            return 'inglés'
        else:
            return 'otro'
    except:
        # Retorna 'desconocido' si no se pudo detectar el idioma
        return 'desconocido'

def process_html_files(input_folder, output_excel):
    """Procesa los archivos HTML y guarda en Excel los que están en español o inglés."""
    # Lista para almacenar URLs y el idioma detectado
    url_data = []

    # Iterar sobre los archivos en la carpeta de entrada
    for filename in os.listdir(input_folder):
        if filename.endswith(".txt"):  # Asegurarse de procesar solo archivos de texto
            file_path = os.path.join(input_folder, filename)
            print(f"Procesando archivo: {filename}")

            # Extraer el texto del archivo HTML
            text = extract_text_from_html(file_path)

            # Detectar el idioma del texto
            detected_language = detect_language_content(text)
            print(f"Idioma detectado en '{filename}': {detected_language}")

            # Solo guardar URLs con contenido en español o inglés
            if detected_language in ['español', 'inglés']:
                # Obtener la URL original del nombre del archivo
                original_url = re.sub(r'^[0-9]+_|_\.txt$', '', filename).replace('_', '/')
                url_data.append({'URL': original_url, 'Idioma': detected_language})

    # Guardar los resultados en un archivo Excel
    df = pd.DataFrame(url_data)
    df.to_excel(output_excel, index=False)
    print(f"Archivo Excel '{output_excel}' creado con URLs en español e inglés.")

# Ejecutar la función principal
process_html_files(input_folder, output_excel)
