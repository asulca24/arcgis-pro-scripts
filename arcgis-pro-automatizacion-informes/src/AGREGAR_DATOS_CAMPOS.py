#"""
Este script actualiza el campo 'UNID' en una serie de shapefiles
con el nombre base de cada shapefile.

Parámetros:
input_folder_with_shapes (str): Ruta a la carpeta que contiene los shapefiles.
shapefiles_to_process (list): Lista de nombres de archivos .shp a procesar.
output_field_name (str): Nombre del campo a actualizar (máximo 10 caracteres).
desired_value_length (int): Longitud máxima de los valores en el campo.
"""


import arcpy
import os

# --- PARÁMETROS A CONFIGURAR ---
# Carpeta donde están tus shapefiles individuales
input_folder_with_shapes = r"C:\Users\lmase\OneDrive\Escritorio\SBN_2025\SECTORES_ASIGNADOS\PIU-41\DIAGNOSTICO INSPECCION\UNIDADES"

# Lista de los nombres de los shapefiles (con su extensión .shp)
# Asegúrate de que esta lista contenga los nombres EXACTOS de tus archivos.
shapefiles_to_process = [
    "PIU-041-03-1.shp",
    "PIU-041-03-2.shp",
    "PIU-041-03-3.shp",
    "PIU-041-03-4.shp",
    "PIU-041-03-5.shp",
    "PIU-041-03-6.shp",
    "PIU-041-03-7.shp"
]

# Nombre del campo para almacenar el ID de la unidad (¡Máximo 10 caracteres para Shapefiles!)
output_field_name = "UNID" 

# Longitud deseada para el valor del campo UNID (ej. "PIU-041-03-7" es 12 caracteres, 25 es seguro)
desired_value_length = 25 

# --- LÓGICA DEL SCRIPT ---
arcpy.env.overwriteOutput = True
arcpy.env.workspace = input_folder_with_shapes # No es estrictamente necesario con rutas completas, pero es buena práctica.

print("Iniciando proceso de corrección de campo 'UNID' usando una lista de shapefiles.")

if not shapefiles_to_process:
    print("ERROR: La lista 'shapefiles_to_process' está vacía. No hay archivos que procesar.")
else:
    print(f"Se procesarán {len(shapefiles_to_process)} shapefiles.")

    for shp_name in shapefiles_to_process:
        full_shp_path = os.path.join(input_folder_with_shapes, shp_name)
        print(f"\n--- Procesando {shp_name} ---")

        # Verificar si el shapefile realmente existe antes de intentar procesarlo
        if not arcpy.Exists(full_shp_path):
            print(f"ADVERTENCIA: El shapefile '{shp_name}' no se encontró en la ruta especificada. Saltando.")
            continue

        try:
            # === Paso 1: Eliminar el campo antiguo 'UNIDAD' si existe ===
            if "UNIDAD" in [f.name for f in arcpy.ListFields(full_shp_path)]:
                print("Eliminando campo 'UNIDAD' antiguo...")
                arcpy.management.DeleteField(full_shp_path, "UNIDAD")

            # === Paso 2: Eliminar el nuevo campo si existe (por si se ejecutó parcialmente) ===
            if output_field_name in [f.name for f in arcpy.ListFields(full_shp_path)]:
                print(f"Eliminando campo '{output_field_name}' existente...")
                arcpy.management.DeleteField(full_shp_path, output_field_name)

            # === Paso 3: Crear el nuevo campo con el nombre corto y la longitud correcta para el valor ===
            print(f"Creando campo '{output_field_name}' con longitud {desired_value_length}...")
            arcpy.management.AddField(full_shp_path, output_field_name, "TEXT", field_length=desired_value_length)

            # === Paso 4: Obtener el valor para el campo (nombre del shapefile sin extensión) ===
            # os.path.splitext(shp_name)[0] toma el nombre del archivo de la lista y quita la extensión.
            unidad_value = os.path.splitext(shp_name)[0]

            # === Paso 5: Calcular el campo recién creado con el valor deseado ===
            print(f"Calculando campo '{output_field_name}' con el valor: '{unidad_value}'...")
            with arcpy.da.UpdateCursor(full_shp_path, [output_field_name]) as cursor:
                for row in cursor:
                    row[0] = unidad_value
                    cursor.updateRow(row)
                    break # Solo una fila por shapefile

            print(f"Campo '{output_field_name}' actualizado correctamente en {shp_name}.")

        except arcpy.ExecuteError:
            print(f"ERROR de ArcPy en {shp_name}: {arcpy.GetMessages(2)}")
            print("Asegúrese de que el shapefile no esté abierto en ArcGIS Pro ni bloqueado por otro proceso.")
        except Exception as e:
            print(f"Error inesperado en {shp_name}: {e}")

print("\nProceso de corrección de campo completado.")