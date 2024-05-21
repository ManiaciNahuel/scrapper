import pandas as pd
from Carrefour import buscador_carrefour
from Farmacity import buscador_farmacity
from Libertad import buscador_libertad
from Lider import buscador_lider
from SuperMami import buscador_superMami


def leer_codigos_desde_excel(archivo_excel):
    try:
        df = pd.read_excel(archivo_excel, header=None)
        codigos = df.iloc[:, 0].tolist()
        nombres_productos = df.iloc[:, 1].tolist()  # Leer la segunda columna con los nombres de los productos
        return codigos, nombres_productos
    except Exception as e:
        print("Error al leer el archivo Excel:", e)
        return [], []

archivo_excel = "codigos.xlsx"
codigos_barra, nombres_productos = leer_codigos_desde_excel(archivo_excel)

# Crear un DataFrame vacío
df_resultados = pd.DataFrame(columns=["Código de Barras", "Sitio", "Producto", "Precio Actual", "Precio Anterior"])

print("---------- Cargando ----------")
for codigo, nombre_producto in zip(codigos_barra, nombres_productos):
    """ print("\n")
    print(f"Buscando productos para el código de barras: {codigo}") """
    
    # Buscar en Carrefour
    resultado_carrefour = buscador_carrefour(codigo)
    if resultado_carrefour["producto"]:
        df_resultados = pd.concat([df_resultados, pd.DataFrame([[codigo, nombre_producto, "Carrefour", resultado_carrefour["precio_actual"], resultado_carrefour["precio_anterior"]]], columns=df_resultados.columns)], ignore_index=True)
    

# Mostrar el DataFrame con los resultados
print(df_resultados)

# Guardar el DataFrame en un archivo CSV
df_resultados.to_csv("resultados_busqueda.csv", index=False)
