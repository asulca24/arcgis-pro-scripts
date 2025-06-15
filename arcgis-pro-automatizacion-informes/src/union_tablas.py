import pandas as pd

# Función para formatear columnas con ceros a la izquierda
def add_leading_zeros(series, length):
    return series.apply(lambda x: str(x).zfill(length))

# Cargar los archivos Excel con manejo de excepciones
try:
    print("Cargando archivo EXCEL_1...")
    excel_1_df = pd.read_excel(r"C:/Users/lmase/OneDrive/Escritorio/ARCHIVOS_EXCEL/sjm_vias/comparativo vias_1.xlsx")
    print("Archivo EXCEL_1 cargado.")
except Exception as e:
    print(f"Error al cargar EXCEL_1: {e}")

try:
    print("Cargando archivo EXCEL_2...")
    excel_2_df = pd.read_excel(r"C:/Users/lmase/OneDrive/Escritorio/ARCHIVOS_EXCEL/sjm_vias/comparativo vias_2.xlsx")
    print("Archivo EXCEL_2 cargado.")
except Exception as e:
    print(f"Error al cargar EXCEL_2: {e}")

# Convertir todas las columnas de ambos DataFrames a tipo string
excel_1_df = excel_1_df.astype(str)
excel_2_df = excel_2_df.astype(str)

# Merge ambos DataFrames en base
merged_df = pd.merge(
    excel_1_df, 
    excel_2_df, 
    left_on=['COD_VIA_1', 'CODIGO_HU_x'], 
    right_on=['COD_VIA_1', 'CODIGO_HU_x'], 
    how='left',
    suffixes=('_left', '_right')
)

# Eliminar duplicados en 'merged_df' 
merged_df.drop_duplicates(inplace=True)

print(merged_df.head())

# Aplicar función de ceros a la izquierda en las columnas relevantes después del merge
#merged_df['CODIGO_VIA_y'] = add_leading_zeros(merged_df['CODIGO_VIA_y_right'], 6)
#merged_df['CODIGO_HU_y'] = add_leading_zeros(merged_df['CODIGO_HU_y_right'], 4)

# Exportar el resultado a un archivo Excel
output_path = r"C:/Users/lmase/OneDrive/Escritorio/ARCHIVOS_EXCEL/sjm_vias/tabla_merge.xlsx"
try:
    merged_df.to_excel(output_path, index=False, header=True)
    print(f"El archivo 'tabla_mejorada.xlsx' ha sido generado con éxito en {output_path}.")
except Exception as e:
    print(f"Error al exportar el archivo Excel: {e}")
