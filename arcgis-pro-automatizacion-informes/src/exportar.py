import pandas as pd

# Cargar los archivos Excel
print("Cargando archivo EXCEL_1...")
excel_1 = pd.read_excel(r"C:/Users/lmase/OneDrive/Escritorio/ARCHIVOS_EXCEL/EXCEL_1_06.xlsx")
print("Archivo EXCEL_1 cargado.")

print("Cargando archivo EXCEL_2...")
excel_2 = pd.read_excel(r"C:/Users/lmase/OneDrive/Escritorio/ARCHIVOS_EXCEL/EXCEL_2_06.xlsx")
print("Archivo EXCEL_2 cargado.")

# Hacer la combinación de datos en base a coincidencia exacta de 'NOMBRE_VIA' y 'NOMBRE_HU'
print("Combinando datos en base a coincidencia de 'NOMBRE_VIA' y 'NOMBRE_HU'...")
merged_data = pd.merge(
    excel_1, 
    excel_2[['CODIGO_VIA', 'NOMBRE_VIA', 'NOMBRE_HU']],
    on=['NOMBRE_VIA', 'NOMBRE_HU'], 
    how='left', 
    suffixes=('_excel1', '_excel2')
)
print("Datos combinados.")

# Verificar las columnas en merged_data
print("Columnas en merged_data:", merged_data.columns)

# Seleccionar solo las columnas necesarias: ID y CODIGO_VIA
result = merged_data[['ID', 'CODIGO_VIA']].fillna('')  # Ajusta 'CODIGO_VIA' si es necesario

# Exportar a archivo Excel
print("Exportando resultado a archivo 'resultado.xlsx'...")
result.to_excel("resultado.xlsx", index=False)
print("Exportación completa.")
