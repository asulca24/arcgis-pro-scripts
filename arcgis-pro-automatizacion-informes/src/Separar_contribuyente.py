import pandas as pd

# Cargar el archivo Excel
print("Cargando archivo EXCEL_1...")
addresses = pd.read_excel(r"C:/Users/lmase/OneDrive/Escritorio/ARCHIVOS_EXCEL/sjm_vias/contribuyente_SJM.xlsx")
print("Archivo EXCEL_1 cargado.")

# Función para extraer MZ, LT, NUM, TIPO_VIA, DESCRIPCION_VIA, TIPO_HU y DESCRIPCION_HU
def extract_details(address):
    if pd.isna(address):
        return None, None, None, None, None, None, None
    parts = str(address).split()
    mz = lt = num = None
    tipo_via = descripcion_via = tipo_hu = descripcion_hu = None
    capturing_via = capturing_hu = False
    vias = ["JR.", "AV.", "CA.", "PJE."]
    hus = ["URB.", "SECT.", "COOP.", "ASOC. VIV.", "AA.HH"]
    current_via = []
    current_hu = []
    
    for i, part in enumerate(parts):
        if part == "MZ.":
            mz = parts[i + 1] if i + 1 < len(parts) else None
            capturing_via = capturing_hu = False
        elif part == "LT.":
            lt = parts[i + 1] if i + 1 < len(parts) else None
            capturing_via = capturing_hu = False
        elif part == "NUM.":
            num = parts[i + 1] if i + 1 < len(parts) else None
            capturing_via = capturing_hu = False
        elif part in vias:
            tipo_via = part
            capturing_via = True
            capturing_hu = False
        elif part in hus:
            tipo_hu = part
            capturing_hu = True
            capturing_via = False
        elif capturing_via:
            current_via.append(part)
        elif capturing_hu:
            current_hu.append(part)
    
    descripcion_via = " ".join(current_via) if current_via else None
    descripcion_hu = " ".join(current_hu) if current_hu else None

    return mz, lt, num, tipo_via, descripcion_via, tipo_hu, descripcion_hu

# Crear un DataFrame con las columnas 'CODIGO DE CONTRIBUYENTE' y 'DOMICILIO FISCAL'
df = addresses[['CODIGO DE CONTRIBUYENTE', 'DOMICILIO FISCAL']].copy()

# Aplicar la función para extraer los detalles
df[['MZ', 'LT', 'NUM', 'TIPO_VIA', 'DESCRIPCION_VIA', 'TIPO_HU', 'DESCRIPCION_HU']] = df['DOMICILIO FISCAL'].apply(lambda x: pd.Series(extract_details(x)))

# Mostrar el DataFrame
print(df)




df.to_excel("resultado_Domicilio.xlsx", index=False)
print("Exportación completa.")