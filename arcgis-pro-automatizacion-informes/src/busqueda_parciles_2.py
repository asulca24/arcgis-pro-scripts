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

# Definir umbrales de coincidencia
umbral_via = 70
umbral_hu = 70

# Usar un bucle para buscar coincidencias para 'NOMBRE_VIA'
mejor_match_via = []
porcentaje_coincidencia_via = []
choices_via = excel_2_df['NOMBRE_VIA'].tolist()
for via in excel_1_df['NOMBRE_VIA']:
    match, score = process.extractOne(via, choices_via, scorer=fuzz.token_sort_ratio)
    if score >= umbral_via:
        mejor_match_via.append(match)
        porcentaje_coincidencia_via.append(score)
    else:
        mejor_match_via.append(None)  # O un valor por defecto
        porcentaje_coincidencia_via.append(0)  # O un valor por defecto

excel_1_df['MEJOR_MATCH_VIA'] = mejor_match_via
excel_1_df['PORCENTAJE_COINCIDENCIA_VIA'] = porcentaje_coincidencia_via

# Usar un bucle para buscar coincidencias para 'NOMBRE_HU'
mejor_match_hu = []
porcentaje_coincidencia_hu = []
choices_hu = excel_2_df['NOMBRE_HU'].tolist()
for hu in excel_1_df['NOMBRE_HU']:
    match, score = process.extractOne(hu, choices_hu, scorer=fuzz.token_sort_ratio)
    if score >= umbral_hu:
        mejor_match_hu.append(match)
        porcentaje_coincidencia_hu.append(score)
    else:
        mejor_match_hu.append(None)  # O un valor por defecto
        porcentaje_coincidencia_hu.append(0)  # O un valor por defecto

excel_1_df['MEJOR_MATCH_HU'] = mejor_match_hu
excel_1_df['PORCENTAJE_COINCIDENCIA_HU'] = porcentaje_coincidencia_hu

# Primer merge en base a 'MEJOR_MATCH_VIA' y 'MEJOR_MATCH_HU'
merged_df = pd.merge(
    excel_1_df, 
    excel_2_df, 
    left_on=['MEJOR_MATCH_HU', 'MEJOR_MATCH_VIA'], 
    right_on=['NOMBRE_HU', 'NOMBRE_VIA'], 
    how='left'
)

# Segundo merge solo para 'CODIGO_HU' en base a 'MEJOR_MATCH_HU'
codigo_hu_only = excel_2_df[['NOMBRE_HU', 'CODIGO_HU']].rename(columns={'CODIGO_HU': 'CODIGO_HU_HU'})
codigo_hu_only = codigo_hu_only.drop_duplicates()

# Merge para añadir solo el CODIGO_HU
merged_df = pd.merge(
    merged_df,
    codigo_hu_only,
    left_on='MEJOR_MATCH_HU',
    right_on='NOMBRE_HU',
    how='left'
)

# Eliminar duplicados
merged_df.drop_duplicates(inplace=True)

# Aplicar función de ceros a la izquierda en las columnas relevantes después del merge
merged_df['CODIGO_VIA'] = add_leading_zeros(merged_df['CODIGO_VIA'], 6)
merged_df['CODIGO_HU_HU'] = add_leading_zeros(merged_df['CODIGO_HU_HU'], 4)

# Exportar el resultado a un archivo Excel
output_path = r"C:/Users/lmase/OneDrive/Escritorio/ARCHIVOS_EXCEL/sjm_vias/tabla_mejorada_4.xlsx"
try:
    merged_df.to_excel(output_path, index=False, header=True)
    print(f"El archivo 'tabla_mejorada.xlsx' ha sido generado con éxito en {output_path}.")
except Exception as e:
    print(f"Error al exportar el archivo Excel: {e}")