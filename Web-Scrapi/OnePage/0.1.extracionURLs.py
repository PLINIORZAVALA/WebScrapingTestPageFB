import re
import pandas as pd

def extract_urls_from_file(file_path):
    """Extrae todas las URLs de un archivo de texto y elimina las repeticiones."""
    # Leer el contenido del archivo
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Usar una expresión regular para encontrar todas las URLs en el contenido
    # Esta expresión regular captura URLs que comienzan con 'http' o 'https' y continuan con cualquier caracter no blanco
    urls = re.findall(r'(https?://[^\s]+)', content)
    
    # Eliminar las URLs duplicadas utilizando un conjunto (set)
    unique_urls = set(urls)
    return unique_urls

def save_urls_to_excel(urls, output_path):
    """Guarda las URLs extraídas en un archivo Excel."""
    # Crear un DataFrame de pandas con las URLs
    df = pd.DataFrame(list(urls), columns=["URL"])
    
    # Guardar el DataFrame en un archivo Excel
    df.to_excel(output_path, index=False)
    print(f"Las URLs se han guardado en {output_path}")

def main():
    # Ruta del archivo de entrada (archivo de texto)
    input_file_path = 'OnePage/0.0.ScrapeoProfundo.txt'
    
    # Ruta del archivo de salida (archivo de Excel)
    output_file_path = 'excelResultProfundo/0.0.urls_extraidas.xlsx'
    
    # Extraer URLs del archivo sin repeticiones
    urls = extract_urls_from_file(input_file_path)
    
    # Guardar las URLs en un archivo Excel
    save_urls_to_excel(urls, output_file_path)

if __name__ == "__main__":
    main()
