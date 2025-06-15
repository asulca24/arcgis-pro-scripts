import geopandas as gpd
from shapely.geometry import LineString, Point
import numpy as np

# 📌 Cargar el archivo con las líneas
input_file = "./DICAPI/50_m_DICAPI.shp"  # Reemplaza con la ruta real
gdf = gpd.read_file(input_file)

# 📌 Función para asegurar que todas las líneas estén orientadas hacia el sur
def ensure_south_orientation(geometry):
    if isinstance(geometry, LineString):
        coords = list(geometry.coords)
        y_start, y_end = coords[0][1], coords[-1][1]
        
        # Si la línea está orientada al norte (inicio en menor Y que el final), invertir
        if y_start < y_end:
            coords.reverse()
        
        return LineString(coords)
    return geometry

# 📌 Aplicar la corrección de orientación
gdf["geometry"] = gdf["geometry"].apply(ensure_south_orientation)

# 📌 Función para detectar vértices de ruptura y generar líneas perpendiculares
def create_perpendiculars_at_breaks(geometry, length=200):
    perpendiculars = []  # Lista para almacenar las líneas generadas
    
    if isinstance(geometry, LineString):
        coords = list(geometry.coords)  # Obtener los vértices de la línea
        
        # Detectar puntos de ruptura (primer y último punto de cada línea)
        start_point, end_point = Point(coords[0]), Point(coords[-1])
        
        for point in [start_point, end_point]:
            # Encontrar dirección de la línea en el punto de ruptura
            if point == start_point and len(coords) > 1:
                ref_point = Point(coords[1])  # Segundo punto de la línea
            elif point == end_point and len(coords) > 1:
                ref_point = Point(coords[-2])  # Penúltimo punto de la línea
            else:
                continue  # Si es un punto aislado, ignorarlo
            
            # Calcular dirección del segmento
            dx, dy = ref_point.x - point.x, ref_point.y - point.y
            
            # Calcular dirección perpendicular (rotación 90°)
            perp_dx, perp_dy = -dy, dx
            
            # Normalizar la longitud a 200 metros
            norm_factor = np.hypot(perp_dx, perp_dy)  # Distancia euclidiana
            perp_dx, perp_dy = (perp_dx / norm_factor) * length, (perp_dy / norm_factor) * length
            
            # Crear la línea perpendicular que inicia en el punto de ruptura
            perpendicular = LineString([
                (point.x, point.y),
                (point.x + perp_dx, point.y + perp_dy)
            ])
            
            perpendiculars.append(perpendicular)

    return perpendiculars

# 📌 Aplicar la función a cada geometría y crear un nuevo GeoDataFrame
all_perpendiculars = []
for geom in gdf["geometry"]:
    all_perpendiculars.extend(create_perpendiculars_at_breaks(geom, length=200))

gdf_perp = gpd.GeoDataFrame(geometry=all_perpendiculars, crs=gdf.crs)

# 📌 Guardar el nuevo shapefile con las líneas perpendiculares
output_file = "./geo/perpendiculares_7.shp"
gdf_perp.to_file(output_file)

print("✅ Proceso completado. Todas las líneas están orientadas hacia el sur y se generaron líneas perpendiculares.")
