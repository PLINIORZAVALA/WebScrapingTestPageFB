import os
import re
from bs4 import BeautifulSoup

# Ruta de entrada (donde están los archivos originales con el HTML completo)
input_dir = 'salida_txtDelExceldeURLs'

# Ruta de salida (donde se guardarán los archivos con solo el texto visible)
output_dir = 'salida_txt_contenido_extraido'

# Crear la carpeta de salida si no existe
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

def extract_text_from_html(html_content):
    # Usar BeautifulSoup para eliminar las etiquetas HTML y extraer solo el texto visible
    soup = BeautifulSoup(html_content, 'html.parser')
    text = soup.get_text(separator='\n', strip=True)

    # Eliminar las URLs o patrones no deseados del texto
    text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
    text = re.sub(r'http://www\.w3\.org/1999/xlink', '', text)

    return text

def process_files():
    # Recorrer todos los archivos en la carpeta de entrada
    for filename in os.listdir(input_dir):
        if filename.endswith('.txt'):
            # Leer el contenido del archivo original
            file_path = os.path.join(input_dir, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                html_content = file.read()

            # Extraer solo el texto visible, limpiando las URLs no deseadas
            text_content = extract_text_from_html(html_content)

            # Guardar el texto extraído en la carpeta de salida
            output_file_path = os.path.join(output_dir, filename)
            with open(output_file_path, 'w', encoding='utf-8') as output_file:
                output_file.write(text_content)

# Ejecutar el proceso
process_files()
