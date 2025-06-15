import pandas as pd
from fuzzywuzzy import fuzz, process

# Función para formatear columnas con ceros a la izquierda
def add_leading_zeros(series, length):
    return series.apply(lambda x: str(x).zfill(length))

# Cargar los archivos Excel con manejo de excepciones
try:
    print("Cargando archivo EXCEL_1...")
    excel_1_df = pd.read_excel(r"C:/Users/lmase/OneDrive/Escritorio/ARCHIVOS_EXCEL/sjm_vias/resultado_Domicilio_1.xlsx")
    print("Archivo EXCEL_1 cargado.")
except Exception as e:
    print(f"Error al cargar EXCEL_1: {e}")

try:
    print("Cargando archivo EXCEL_2...")
    excel_2_df = pd.read_excel(r"C:/Users/lmase/OneDrive/Escritorio/ARCHIVOS_EXCEL/sjm_vias/TABLA_GIS.xlsx")
    print("Archivo EXCEL_2 cargado.")
except Exception as e:
    print(f"Error al cargar EXCEL_2: {e}")

# Convertir todas las columnas de ambos DataFrames a tipo string
excel_1_df = excel_1_df.astype(str)
excel_2_df = excel_2_df.astype(str)

# Buscar coincidencias basadas en similitud de texto
def find_best_match(row, choices, column):
    match, score = process.extractOne(row[column], choices, scorer=fuzz.token_sort_ratio)
    return pd.Series([match, score])

# Aplicar función de coincidencias aproximadas para 'NOMBRE_VIA' y 'NOMBRE_HU'
choices_via = excel_2_df['NOMBRE_VIA'].tolist()
choices_hu = excel_2_df['NOMBRE_HU'].tolist()

excel_1_df[['MEJOR_MATCH_VIA', 'PORCENTAJE_COINCIDENCIA_VIA']] = excel_1_df.apply(find_best_match, choices=choices_via, column='NOMBRE_VIA', axis=1)
excel_1_df[['MEJOR_MATCH_HU', 'PORCENTAJE_COINCIDENCIA_HU']] = excel_1_df.apply(find_best_match, choices=choices_hu, column='NOMBRE_HU', axis=1)

# Merge ambos DataFrames en base a 'MEJOR_MATCH_VIA' y 'MEJOR_MATCH_HU'
merged_df = pd.merge(
    excel_1_df, 
    excel_2_df, 
    left_on=['MEJOR_MATCH_HU', 'MEJOR_MATCH_VIA'], 
    right_on=['NOMBRE_HU', 'NOMBRE_VIA'], 
    how='left'
)

# Eliminar duplicados en 'merged_df' 
merged_df.drop_duplicates(inplace=True)

# Aplicar función de ceros a la izquierda en las columnas relevantes después del merge
merged_df['CODIGO_VIA'] = add_leading_zeros(merged_df['CODIGO_VIA'], 6)
merged_df['CODIGO_HU'] = add_leading_zeros(merged_df['CODIGO_HU'], 4)

# Renombrar columnas para mayor claridad
merged_df.rename(columns={'CODIGO_VIA_y': 'CODIGO_VIA', 'CODIGO_HU_y': 'CODIGO_HU'}, inplace=True)

# Exportar el resultado a un archivo Excel
output_path = r"C:/Users/lmase/OneDrive/Escritorio/ARCHIVOS_EXCEL/sjm_vias/tabla_mejorada_4.xlsx"
try:
    merged_df.to_excel(output_path, index=False, header=True)
    print(f"El archivo 'tabla_mejorada.xlsx' ha sido generado con éxito en {output_path}.")
except Exception as e:
    print(f"Error al exportar el archivo Excel: {e}")
