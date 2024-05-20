import pandas as pd
from Carrefour import buscador_carrefour
from Farmacity import buscador_farmacity
from Libertad import buscador_libertad
from Lider import buscador_lider
from SuperMami import buscador_superMami

def leer_codigos_desde_excel(archivo_excel):
    try:
        # Lee el archivo Excel y obtiene los códigos de barras de la primera columna
        df = pd.read_excel(archivo_excel, header=None)  # Sin encabezados
        codigos = df.iloc[:, 0].tolist()  # Toma solo la primera columna
        return codigos
    except Exception as e:
        print("Error al leer el archivo Excel:", e)
        return []

archivo_excel = "codigos.xlsx"  # Ruta de tu archivo Excel
codigos_barra = leer_codigos_desde_excel(archivo_excel)

for codigo in codigos_barra:
    print("\n")
    print(f"Buscando productos para el código de barras: {codigo}")
    buscador_carrefour(codigo)
    print("\n")
    buscador_libertad(codigo)
    print("\n")
    buscador_lider(codigo)
    print("\n")
    buscador_superMami(codigo)
    print("\n")
    buscador_farmacity(codigo)
