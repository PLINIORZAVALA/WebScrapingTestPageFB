import re
import pandas as pd
from bs4 import BeautifulSoup

# Paso 1: Leer el contenido del archivo .txt con el HTML o texto sin procesar
with open('OnePage/0.0.consola_output.txt', 'r', encoding='utf-8') as file:
    html_content = file.read()

# Paso 2: Utilizar BeautifulSoup para parsear el HTML
soup = BeautifulSoup(html_content, 'html.parser')

# Paso 3: Extraer las imágenes con sus atributos (alt, title, src)
images_data = []
for img in soup.find_all('img'):
    alt = img.get('alt', 'N/A')
    title = img.get('title', 'N/A')
    src = img.get('src', 'N/A')
    images_data.append({'Alt': alt, 'Title': title, 'Src': src})

# Paso 4: Extraer las fechas del div con clase 'poster_star_s'
fechas_data = []
for div in soup.find_all('div', class_='poster_star_s'):
    fecha = div.get_text(strip=True)  # Elimina espacios en blanco alrededor
    fechas_data.append({'Fechas': fecha})

# Paso 5: Extraer el tipo de evento del div con clase 'poster_tag'
eventos_data = []
for div in soup.find_all('div', class_='poster_tag'):
    evento = div.get_text(strip=True)
    eventos_data.append({'Evento': evento})

# Paso 6: Extraer el lugar del p con los enlaces y texto adicional
lugares_data = []
for p in soup.find_all('p', style=re.compile(r'width: 100%;float: left;padding-left:0px;')):
    lugar_a = p.find('a')
    lugar_span = p.find('span', style='font-style: italic;')
    lugar_nombre = lugar_a.get_text(strip=True) if lugar_a else 'N/A'
    lugar_descripcion = lugar_span.get_text(strip=True) if lugar_span else 'N/A'
    lugares_data.append({'Lugar': f'{lugar_nombre} - {lugar_descripcion}'})

# Paso 7: Extraer el lugar geográfico conocido (contenido en <span> con estilo en cursiva)
lugares_geograficos_data = []
for span in soup.find_all('span', style='font-style: italic;'):
    lugar_geografico = span.get_text(strip=True)
    if lugar_geografico and lugar_geografico != lugar_descripcion:  # Aseguramos que no se repita el mismo lugar
        lugares_geograficos_data.append({'Lugar Geográfico': lugar_geografico})

# Paso 8: Organizar los datos relevantes en un DataFrame de Pandas
df_images = pd.DataFrame(images_data)
df_fechas = pd.DataFrame(fechas_data)
df_eventos = pd.DataFrame(eventos_data)
df_lugares = pd.DataFrame(lugares_data)
df_lugares_geograficos = pd.DataFrame(lugares_geograficos_data)

# Unir los DataFrames por el índice (esto puede ser ajustado según el caso)
df_combined = pd.concat([df_images, df_fechas, df_eventos, df_lugares, df_lugares_geograficos], axis=1)

# Paso 9: Limpiar los datos (si es necesario)
df_combined.drop_duplicates(inplace=True)  # Eliminar duplicados si los hay
df_combined.fillna('N/A', inplace=True)  # Reemplazar valores faltantes con 'N/A'

# Paso 10: Guardar el DataFrame como un archivo Excel (.xlsx)
df_combined.to_excel('datos_combinados.xlsx', index=False)

# Mostrar el DataFrame combinado en la consola
print(df_combined)
