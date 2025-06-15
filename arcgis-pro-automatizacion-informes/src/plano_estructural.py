import ezdxf

def crear_distribucion_columnas(nombre_archivo, longitud, ancho, separacion_longitudinal, separacion_filas):
    # Crear un nuevo documento DXF
    doc = ezdxf.new()
    # Obtener el espacio modelo
    msp = doc.modelspace()
    
    # Parámetros para las filas
    fila1_y = 1.5  # Primera fila, 1.5 metros desde el borde
    fila2_y = fila1_y + separacion_filas  # Segunda fila, separada 2 metros
    
    # Coordenadas iniciales y cálculo del número de columnas
    x = 0
    num_columnas = int(longitud / separacion_longitudinal) + 1
    
    # Tamaño del cuadrado
    ancho_cuadrado = 0.25  # 0.25 m de ancho
    alto_cuadrado = 0.35    # 0.35 m de alto

    # Crear las columnas
    for i in range(num_columnas):
        # Agregar columna a la primera fila (cuadrado rojo)
        msp.add_lwpolyline(points=[
            (x - ancho_cuadrado / 2, fila1_y - alto_cuadrado / 2),
            (x + ancho_cuadrado / 2, fila1_y - alto_cuadrado / 2),
            (x + ancho_cuadrado / 2, fila1_y + alto_cuadrado / 2),
            (x - ancho_cuadrado / 2, fila1_y + alto_cuadrado / 2),
            (x - ancho_cuadrado / 2, fila1_y - alto_cuadrado / 2)  # Cerrar el polígono
        ], close=True, dxfattribs={"color": 1})  # Rojo para fila 1

        # Agregar columna a la segunda fila (cuadrado verde)
        msp.add_lwpolyline(points=[
            (x - ancho_cuadrado / 2, fila2_y - alto_cuadrado / 2),
            (x + ancho_cuadrado / 2, fila2_y - alto_cuadrado / 2),
            (x + ancho_cuadrado / 2, fila2_y + alto_cuadrado / 2),
            (x - ancho_cuadrado / 2, fila2_y + alto_cuadrado / 2),
            (x - ancho_cuadrado / 2, fila2_y - alto_cuadrado / 2)  # Cerrar el polígono
        ], close=True, dxfattribs={"color": 3})  # Verde para fila 2

        # Avanzar a la siguiente columna
        x += separacion_longitudinal

    # Guardar el archivo DXF
    doc.saveas(nombre_archivo)
    print(f"Archivo DXF guardado como {nombre_archivo}")

# Parámetros del terreno y columnas
longitud_terreno = 20  # Longitud en metros
ancho_terreno = 4      # Ancho en metros
separacion_columnas = 4  # Separación entre columnas en la fila
separacion_filas = 2     # Separación entre filas

# Nombre del archivo DXF
archivo_dxf = "./distribucion_columnas.dxf"
# Crear el archivo DXF con la distribución de columnas
crear_distribucion_columnas(archivo_dxf, longitud_terreno, ancho_terreno, separacion_columnas, separacion_filas)