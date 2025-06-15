import arcpy

# Define parámetros básicos
output_folder = r'C:\ruta\a\tu\carpeta'
shapefile_name = "poligonos.shp"
mxd_output = r'C:\ruta\a\tu\archivo.mxd'

# Crear un shapefile vacío
arcpy.CreateFeatureclass_management(output_folder, shapefile_name, "POLYGON")

# Agregar campos para almacenar medidas y ángulos
arcpy.AddField_management(f"{output_folder}\\{shapefile_name}", "Perimetro", "DOUBLE")
arcpy.AddField_management(f"{output_folder}\\{shapefile_name}", "Area", "DOUBLE")
arcpy.AddField_management(f"{output_folder}\\{shapefile_name}", "Angulo", "TEXT")

# Insertar un ejemplo de polígono y calcular medidas
cursor = arcpy.da.InsertCursor(f"{output_folder}\\{shapefile_name}", ['SHAPE@'])
array = arcpy.Array([arcpy.Point(0, 0), arcpy.Point(1, 0), arcpy.Point(1, 1), arcpy.Point(0, 1), arcpy.Point(0, 0)])
polygon = arcpy.Polygon(array)
cursor.insertRow([polygon])

del cursor

# Calcular perímetro, área y ángulos
with arcpy.da.UpdateCursor(f"{output_folder}\\{shapefile_name}", ['SHAPE@', 'Perimetro', 'Area', 'Angulo']) as cursor:
    for row in cursor:
        row[1] = row[0].length  # Perímetro
        row[2] = row[0].area  # Área
        row[3] = "90°,90°,90°,90°"  # Ejemplo: ángulos predeterminados
        cursor.updateRow(row)

# Crear un mapa (archivo .mxd)
mxd = arcpy.mapping.MapDocument("CURRENT")
df = arcpy.mapping.ListDataFrames(mxd)[0]
layer = arcpy.mapping.Layer(f"{output_folder}\\{shapefile_name}")
arcpy.mapping.AddLayer(df, layer)

mxd.saveACopy(mxd_output)
print(f"Archivo .mxd guardado en {mxd_output}")
