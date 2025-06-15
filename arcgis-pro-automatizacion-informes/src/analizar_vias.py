import pandas as pd

# Cargar el archivo Excel
ruta_archivo = r"C:/Users/lmase/OneDrive/Escritorio/ARCHIVOS_EXCEL/tabla_san martin_1811_2.xlsx"
df = pd.read_excel(ruta_archivo)

# Convertir la columna NUMERO a numérica, manejando errores
df["NUMERO"] = pd.to_numeric(df["NUMERO"], errors="coerce")

# Eliminar filas donde NUMERO no sea un valor numérico
df = df.dropna(subset=["NUMERO"])

# Asegurarse de que NUMERO sea de tipo entero
df["NUMERO"] = df["NUMERO"].astype(int)

# Función para detectar números fuera de la secuencia considerando un rango de 99
def detectar_fuera_de_secuencia_por_grupo(df, rango=99):
    resultados = []
    for grupo, datos_grupo in df.groupby("COD_VIA"):
        numeros = sorted(datos_grupo["NUMERO"])
        for i in range(len(numeros)):
            # Verificar si no hay ningún número en el rango [-rango, +rango] alrededor del número actual
            dentro_de_rango = any(
                abs(numeros[i] - numeros[j]) <= rango for j in range(len(numeros)) if i != j
            )
            if not dentro_de_rango:
                # Agregar a los resultados si no hay vecinos en el rango permitido
                id_correspondiente = datos_grupo[datos_grupo["NUMERO"] == numeros[i]]["ID"].values[0]
                resultados.append((id_correspondiente, numeros[i], grupo))
    return pd.DataFrame(resultados, columns=["ID", "NUMERO", "COD_VIA"])

# Aplicar la función al DataFrame
resultado_final = detectar_fuera_de_secuencia_por_grupo(df, rango=99)

# Guardar los resultados en un nuevo archivo Excel
ruta_salida = r"C:/Users/lmase/OneDrive/Escritorio/ARCHIVOS_EXCEL/tabla_san martin_RESULTADOS.xlsx"
resultado_final.to_excel(ruta_salida, index=False)

print(f"Resultados guardados en {ruta_salida}")
