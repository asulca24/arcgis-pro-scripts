import pandas as pd
import re
from difflib import SequenceMatcher

# Lista de palabras comunes que queremos excluir de los nombres
stop_words = {"de", "del", "el", "la", "los", "las", "y", "a", "en", "por", "con", "sin"}

# Función para limpiar y procesar el nombre de la vía
def limpiar_nombre_via(nombre):
    if pd.isna(nombre):
        return ""  # Si el valor es nulo, devolver una cadena vacía
    nombre = str(nombre).lower()  # Convertir a cadena de texto y a minúsculas
    palabras = nombre.split()
    palabras_filtradas = [palabra for palabra in palabras if palabra not in stop_words]
    return " ".join(palabras_filtradas)

# Función para encontrar la mejor coincidencia exacta entre dos cadenas
def obtener_mejor_coincidencia(nombre, lista_nombres):
    # Primero, comprobamos si ya existe una coincidencia exacta
    if nombre in lista_nombres.values:
        return nombre  # Si ya existe una coincidencia exacta, la devolvemos
    return None  # Si no hay coincidencia exacta, devolvemos None

# Cargar los archivos Excel
print("Cargando archivo EXCEL_1...")
excel_1 = pd.read_excel(r"C:/Users/lmase/OneDrive/Escritorio/ARCHIVOS_EXCEL/EXCEL_1_06.xlsx")
print("Archivo EXCEL_1 cargado.")

print("Cargando archivo EXCEL_2...")
excel_2 = pd.read_excel(r"C:/Users/lmase/OneDrive/Escritorio/ARCHIVOS_EXCEL/EXCEL_2_06.xlsx")
print("Archivo EXCEL_2 cargado.")

# Limpiar los nombres de las vías en ambos DataFrames
print("Limpiando nombres de vías...")
excel_1['NOMBRE_VIA'] = excel_1['NOMBRE_VIA'].fillna('')  # Rellenar valores nulos con cadenas vacías
excel_1['NOMBRE_VIA_LIMPIO'] = excel_1['NOMBRE_VIA'].apply(limpiar_nombre_via)
excel_2['NOMBRE_VIA_LIMPIO'] = excel_2['NOMBRE_VIA'].apply(limpiar_nombre_via)
print("Nombres de vías limpios.")

# Buscar coincidencias exactas entre los nombres limpios de ambas tablas considerando el codigo_hu
print("Buscando coincidencias exactas entre los nombres de vías...")
coincidencias = []

for index_1, row_1 in excel_1.iterrows():
    # Filtramos solo aquellos registros que tengan el mismo codigo_hu en ambos DataFrames
    excel_2_filtrado = excel_2[excel_2['CODIGO_HU'] == row_1['CODIGO_HU']]
    
    if not excel_2_filtrado.empty:
        # Buscar la mejor coincidencia exacta dentro del filtro por CODIGO_HU
        mejor_coincidencia = obtener_mejor_coincidencia(row_1['NOMBRE_VIA_LIMPIO'], excel_2_filtrado['NOMBRE_VIA_LIMPIO'])
        
        if mejor_coincidencia:
            # Obtener el código de la vía correspondiente de EXCEL_2
            codigo_via = excel_2_filtrado[excel_2_filtrado['NOMBRE_VIA_LIMPIO'] == mejor_coincidencia]['CODIGO_VIA'].iloc[0]
            coincidencias.append({
                'ID_1': row_1['ID'],  # Suponiendo que la columna ID esté presente en EXCEL_1
                'CODIGO_VIA': codigo_via,
                'CODIGO_HU': row_1['CODIGO_HU'],
                'NOMBRE_VIA_1': row_1['NOMBRE_VIA'],
                'NOMBRE_VIA_2': mejor_coincidencia
            })

# Convertir las coincidencias en un DataFrame para exportar
coincidencias_df = pd.DataFrame(coincidencias)

# Exportar las coincidencias a un archivo de texto
print("Exportando coincidencias a archivo TXT...")
coincidencias_df.to_csv(r"C:/Users/lmase/OneDrive/Escritorio/ARCHIVOS_EXCEL/coincidencias_vias.txt", sep='\t', index=False)
print("Archivo exportado con coincidencias.")
