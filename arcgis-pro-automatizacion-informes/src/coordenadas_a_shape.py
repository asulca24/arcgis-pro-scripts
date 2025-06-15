import pandas as pd
import geopandas as gpd
from shapely.geometry import Polygon

# Cargar el archivo Excel
file_path = r"./COORDENADAS_CUS_129172.xlsx"  # Reemplaza con la ruta correcta
df = pd.read_excel(file_path, sheet_name="Hoja1")  # Asegura el nombre de la hoja

# Verificar nombres de las columnas
print("Columnas disponibles en el archivo Excel:", df.columns)

# Extraer coordenadas X (Este) y Y (Norte)
coordinates = list(zip(df["Este"], df["Norte"]))

# Crear un polígono con las coordenadas
polygon = Polygon(coordinates)

# Crear un GeoDataFrame
gdf = gpd.GeoDataFrame({"id": [1]}, geometry=[polygon], crs="EPSG:32717")

# Guardar como archivo SHP
shp_path = "./geo/CUS_129172.shp"  # Reemplaza con la ruta deseada
gdf.to_file(shp_path, driver="ESRI Shapefile")

print("Archivo SHP guardado en:", shp_path)
