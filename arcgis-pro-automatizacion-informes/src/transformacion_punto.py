import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

# Ruta del archivo CSV
ARCHIVOS_EXCEL = './geo/tabla_direcciones.xlsx'  # Cambia esta ruta a tu archivo

# Leer el CSV con pandas
df=pd.read_excel(ARCHIVOS_EXCEL)

print(df.dtypes)

# Convertir LATITUD y LONGITUD a valores decimales (dividiendo por 10^6)- USAR EN CAS
#df['LATITUD'] = df['LATITUD'] / 1e4
#df['LONGITUD'] = df['LONGITUD'] / 1e4

print (df)

# Reemplazar comas por puntos en 'LONGITUD' y 'LATITUD'
#df['LONGITUD'] = df['LONGITUD'].str.replace(',', '.', regex=False)
#df['LATITUD'] = df['LATITUD'].str.replace(',', '.', regex=False)

# Convertir las columnas a tipos numéricos
df['Longitud'] = pd.to_numeric(df['Longitud'], errors='coerce')
df['Latitud'] = pd.to_numeric(df['Latitud'], errors='coerce')

print (df)


# Verificar que no haya valores NaN o no válidos
df = df.dropna(subset=['Latitud', 'Longitud'])

# Crear la geometría de puntos usando las columnas Longitud y Latitud
geometry = [Point(xy) for xy in zip(df['Longitud'], df['Latitud'])]

# Crear el GeoDataFrame, incluyendo el campo 'NOMBRE' como atributo
gdf = gpd.GeoDataFrame(df[['Direcciones']], geometry=geometry, crs="EPSG:4326")

print(gdf)

# Guardar el resultado como un Shapefile con las coordenadas WGS 84
gdf.to_file("./geo/puntos_georreferenciados_0912_11.shp", driver='ESRI Shapefile')

print("Shapefile creado correctamente con coordenadas WGS 84.")
