import pandas as pd
#Función para formatear columnas con ceros a la izquierda 
def add_leading_zeros(series, length): return series.apply(lambda x: str(x).zfill(length))

# Cargar los archivos Excel
print("Cargando archivo EXCEL_1...")
excel_1_df = pd.read_excel(r"C:/Users/lmase/OneDrive/Escritorio/ARCHIVOS_EXCEL/sjm_vias/resultado_Domicilio_1.xlsx")
print("Archivo EXCEL_1 cargado.")

print("Cargando archivo EXCEL_2...")
excel_2_df = pd.read_excel(r"C:/Users/lmase/OneDrive/Escritorio/ARCHIVOS_EXCEL/sjm_vias/TABLA_GIS.xlsx")
print("Archivo EXCEL_2 cargado.")

# Convertir 'CODIGO_HU' y 'NOMBRE_VIA' a tipo string en ambos DataFrames para asegurar coincidencias
#excel_1_df['NOMBRE_HU'] = excel_1_df['NOMBRE_HU'].astype(str)
#excel_2_df['NOMBRE_HU'] = excel_2_df['NOMBRE_HU'].astype(str)
#excel_1_df['NOMBRE_VIA'] = excel_1_df['NOMBRE_VIA'].astype(str)
#excel_2_df['NOMBRE_VIA'] = excel_2_df['NOMBRE_VIA'].astype(str)
excel_1_df = excel_1_df.astype(str) 
excel_2_df = excel_2_df.astype(str)

# Merge ambos DataFrames en base a 'CODIGO_HU' y 'NOMBRE_VIA'
merged_df = pd.merge(
    excel_1_df, 
    excel_2_df, 
    on=['NOMBRE_HU', 'NOMBRE_VIA'], 
    how='left'
)

# Aplicar función de ceros a la izquierda en las columnas relevantes después del merge 
merged_df['CODIGO_VIA'] = add_leading_zeros(merged_df['CODIGO_VIA'], 6) 
merged_df['CODIGO_HU'] = add_leading_zeros(merged_df['CODIGO_HU'], 4)

# Seleccionar solo las columnas 'ID' y 'CODIGO_VIA' para el resultado
resultado_df = merged_df

# Exportar el resultado a un archivo de texto
resultado_df.to_excel(r"C:/Users/lmase/OneDrive/Escritorio/ARCHIVOS_EXCEL/sjm_vias/TABLA_FINAL_1.xlsx",index=False, header=True)


print("El archivo 'resultado_codigos_via.txt' ha sido generado con éxito en el escritorio.")
