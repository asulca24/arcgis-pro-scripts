import pandas as pd
from geopy.geocoders import Nominatim
import time
import geopandas as gpd
from shapely.geometry import Point

# Ruta del archivo de Excel
ruta_excel = './geo/tabla_direcciones.xlsx'  # Cambia esta ruta a tu archivo

# Lee el archivo de Excel
df = pd.read_excel(ruta_excel)

print(df.columns)


# Configura el geolocalizador
geolocator = Nominatim(user_agent="tu_aplicacion")

# Función para obtener coordenadas
def obtener_coordenadas(direccion):
    try:
        location = geolocator.geocode(direccion)
        if location:
            return location.latitude, location.longitude
        else:
            return None, None
    except Exception as e:
        print(f"Error con la dirección {direccion}: {e}")
        return None, None

# Añadir nuevas columnas para latitud y longitud
df['Latitud'] = None
df['Longitud'] = None

# Recorre las direcciones y obtiene las coordenadas
for i, direccion in enumerate(df['Direcciones']):
    lat, lng = obtener_coordenadas(direccion)
    df.at[i, 'Latitud'] = lat
    df.at[i, 'Longitud'] = lng
    if (i + 1) % 100 == 0:  # Pausa cada 100 solicitudes
        time.sleep(1)  # Ajusta el tiempo según sea necesario

# Guardar el resultado en un nuevo archivo de Excel
ruta_excel_salida = './geo/archivo_con_coordenadas.xlsx'
df.to_excel(ruta_excel_salida, index=False)

print("Coordenadas añadidas correctamente y guardadas en el nuevo archivo")

# Crear GeoDataFrame con las coordenadas obtenidas
# Verificar que no haya valores NaN o no válidos
df = df.dropna(subset=['Latitud', 'Longitud'])

# Crear la geometría de puntos usando las columnas Longitud y Latitud
geometry = [Point(xy) for xy in zip(df['Longitud'], df['Latitud'])]

# Crear el GeoDataFrame, incluyendo el campo 'NOMBRE' como atributo
gdf = gpd.GeoDataFrame(df[['Direcciones']], geometry=geometry, crs="EPSG:4326")

# Guardar el resultado como un Shapefile con las coordenadas WGS 84
gdf.to_file("./geo/puntos_georreferenciados_todos_1212.shp", driver='ESRI Shapefile')

print("Shapefile creado correctamente con coordenadas WGS 84.")
