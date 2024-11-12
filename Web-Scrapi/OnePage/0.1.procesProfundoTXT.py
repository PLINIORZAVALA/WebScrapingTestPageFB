import re
import pandas as pd

def extract_urls_from_file(filename):
    # Lee el contenido del archivo de texto
    with open(filename, 'r', encoding='utf-8') as file:
        html_content = file.read()
    
    # Usa una expresión regular para encontrar todas las URLs
    url_pattern = re.compile(r'https?://[^\s"\'>]+')
    urls = url_pattern.findall(html_content)
    
    # Remover duplicados, en caso de que haya URLs repetidas
    unique_urls = list(set(urls))
    return unique_urls

def save_urls_to_excel(urls, output_filename):
    # Convierte las URLs en un DataFrame de pandas
    df = pd.DataFrame(urls, columns=['URL'])
    
    # Guarda el DataFrame en un archivo Excel
    df.to_excel(output_filename, index=False)

# ---------------------- Código Principal ----------------------

def main():
    # Nombre del archivo de texto generado anteriormente
    input_filename = 'OnePage/0.0.ScrapeoProfundo.txt'
    
    # Nombre del archivo Excel de salida
    output_filename = 'excelResultProfundo/0.0.urls_extraidas.xlsx'
    
    # Extrae las URLs y guárdalas en un archivo Excel
    urls = extract_urls_from_file(input_filename)
    save_urls_to_excel(urls, output_filename)
    print(f"Las URLs se han extraído y guardado en '{output_filename}'.")

if __name__ == "__main__":
    main()
