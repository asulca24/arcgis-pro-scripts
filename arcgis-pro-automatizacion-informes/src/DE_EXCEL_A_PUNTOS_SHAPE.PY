import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

# Ruta del archivo Excel
archivo_excel = './coord_CONCESION.xlsx'  # Cambia esta ruta a tu archivo

# Leer el Excel con pandas
df = pd.read_excel(archivo_excel, sheet_name="Hoja1")

# Renombrar las columnas para asegurarse de que no haya espacios en blanco
df.rename(columns=lambda x: x.strip(), inplace=True)

print(df.head())  # Esto debería mostrar las columnas sin espacios en blanco

# Crear la geometría de puntos usando las columnas Este y Norte
geometry = [Point(xy) for xy in zip(df['Este'], df['Norte'])]

# Crear el GeoDataFrame, incluyendo el campo 'VERTICE' como atributo
gdf = gpd.GeoDataFrame(df[['VERTICE']], geometry=geometry, crs="EPSG:32717")

# Guardar el resultado como un Shapefile con las coordenadas WGS 84 (sin transformar)
gdf.to_file("./geo/CONSESION2.shp", driver='ESRI Shapefile')

print("Shapefile creado correctamente con coordenadas wgs.")
