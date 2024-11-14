import os
from langdetect import detect

# Ruta de entrada (donde están los archivos con el contenido extraído)
input_dir = '0.3.salida_txt_contenido_extraido'

# Rutas de salida para los documentos en español e inglés
output_dir_spanish = '0.4.salida_txt_espanol'
output_dir_english = '0.4.salida_txt_ingles'

# Crear las carpetas de salida si no existen
if not os.path.exists(output_dir_spanish):
    os.makedirs(output_dir_spanish)

if not os.path.exists(output_dir_english):
    os.makedirs(output_dir_english)

def detect_language(text):
    try:
        # Detectar el idioma del texto
        language = detect(text)
        return language
    except:
        return None  # En caso de error en la detección, se considera como desconocido

def process_files():
    # Recorrer todos los archivos en la carpeta de entrada
    for filename in os.listdir(input_dir):
        if filename.endswith('.txt'):
            # Leer el contenido del archivo
            file_path = os.path.join(input_dir, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                text_content = file.read()

            # Detectar el idioma del texto
            language = detect_language(text_content)

            # Si el texto está en español, guardarlo en la carpeta correspondiente con el mismo nombre
            if language == 'es':
                output_file_path = os.path.join(output_dir_spanish, filename)
                with open(output_file_path, 'w', encoding='utf-8') as output_file:
                    output_file.write(text_content)
            
            # Si el texto está en inglés, guardarlo en la carpeta correspondiente con el mismo nombre
            elif language == 'en':
                output_file_path = os.path.join(output_dir_english, filename)
                with open(output_file_path, 'w', encoding='utf-8') as output_file:
                    output_file.write(text_content)

# Ejecutar el proceso
process_files()
