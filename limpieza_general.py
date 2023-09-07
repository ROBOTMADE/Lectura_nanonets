import os
import pandas as pd
from tqdm import tqdm
from config import *

def procesar(df: pd.DataFrame):
    # Copiar los datos del DataFrame
    datos_nanonets = df.copy()

    # Filtrar valores no deseados de los contenedores
    for contenedor in contenedores:
        if contenedor in datos_nanonets.columns:
            for valor in contenedores[contenedor]:
                datos_nanonets = datos_nanonets[~datos_nanonets[contenedor].astype(str).str.upper().str.contains(valor.upper())]

    # Procesar datos de factura específica
    ultima_factura = ""
    for index, row in tqdm(datos_nanonets.iterrows(), total=datos_nanonets.shape[0]):
        if ultima_factura != row["ruta_factura"]:
            ultima_factura = row["ruta_factura"]
            datos_factura_especifica = datos_nanonets[datos_nanonets["ruta_factura"].astype(str) == row['ruta_factura']]
            print()

            for index_factura, row_factura in datos_factura_especifica.iterrows():
                try:
                    borrar = True
                    for columna in columnas_tabla:
                        if columna in datos_factura_especifica.columns and not pd.isna(row_factura[columna]):
                            borrar = False
                            break

                    if borrar:
                        datos_nanonets.loc[index_factura - 1, "descripcion"] = f'{datos_nanonets.loc[index_factura - 1, "descripcion"]}{row_factura["descripcion"]}'
                        datos_nanonets.drop([index_factura], inplace=True)
                except Exception as e:
                    print(e)

    # Verificar si la columna "descripcion" está presente
    if "descripcion" in datos_nanonets.columns:
        datos_nanonets = datos_nanonets[datos_nanonets["descripcion"].astype(str).str.len() > 2]

    # Crear directorio de salida si no existe
    output_directory = f"Salida/{version_lectura}"
    if not os.path.isdir(output_directory):
        os.makedirs(output_directory)

    # Guardar resultados en un archivo Excel
    output_file = os.path.join(output_directory, "limpieza_general.xlsx")
    datos_nanonets.to_excel(output_file, index=None)

    return datos_nanonets

# Ejemplo de uso
# df = ... # Cargar tu DataFrame
# procesado = procesar(df)
