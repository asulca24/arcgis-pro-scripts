import arcpy
import os
import re

# Definir la capa de entrada
input_fc = "PIU_037_UNIDADES"  # Nombre exacto de la capa cargada en ArcGIS Pro
field_name = "UNIDAD"  # Campo que contiene los nombres de salida

# Definir la carpeta donde se guardarán los archivos .shp
output_folder = r"C:\Users\lmase\OneDrive\Escritorio\PIU_037_UNIDADES"  # Cambia esta ruta a la carpeta deseada
if not os.path.exists(output_folder):
    os.makedirs(output_folder)  # Crear la carpeta si no existe

# Establecer entorno de trabajo para evitar conflictos
arcpy.env.workspace = output_folder
arcpy.env.overwriteOutput = True

# Recorrer los registros de la capa y exportar cada polígono como archivo .shp
with arcpy.da.SearchCursor(input_fc, ["SHAPE@", field_name]) as cursor:
    for row in cursor:
        shape = row[0]
        unit_name = row[1]

        # Limpiar el nombre eliminando caracteres inválidos
        unit_name_clean = re.sub(r"[^a-zA-Z0-9_]", "_", unit_name)[:30]  # Máximo 30 caracteres
        output_shp = os.path.join(output_folder, f"{unit_name_clean}.shp")

        # Exportar cada polígono como archivo .shp
        arcpy.CopyFeatures_management(shape, output_shp)
        print(f"Archivo '{unit_name_clean}.shp' exportado correctamente.")

print("Proceso finalizado. Todos los archivos .shp se han guardado en la carpeta especificada.")