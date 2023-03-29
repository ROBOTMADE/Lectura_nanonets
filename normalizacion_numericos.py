import datetime

import pandas as pd
import re
from config import *
from dateutil import parser
diccionario_meses = {
    "ENE" : "01",
    "FEB" : "02",
    "MAR": "03",
    "ABR": "04",
    "MAY": "05",
    "JUN": "06",
    "JUL": "07",
    "AGO": "08",
    "SEP": "09",
    "OCT": "10",
    "NOV": "11",
    "DIC": "12",


}
def procesar(df):
    valores_numericos = ["cantidad", "total", "iva_factura", "valor_total_factura", "subtotal_factura", "iva",
                         "descuento", "valor_unitario"]
    valores_fecha = ["fecha_factura"]
    combinacion_formatos = ""
    for columna_numerica in valores_numericos:
        if not columna_numerica in df.columns:
            valores_numericos.remove(columna_numerica)
        else:
            df[columna_numerica].fillna(0, inplace=True)


    for index, row in df.iterrows():
        for columna_numerica in valores_numericos:

            valor = str(row[columna_numerica])

            valor_original = valor
            valor = valor.replace("$ ", "")
            #valor = valor.replace("$", "")
            if valor.count(",") == 1:
                valor = valor.replace(",", ".")
            if valor.count(".") > 1:
                valor = "".join(valor.split(".")[:-1])
            if valor.count(",") > 1:
                valor = "".join(valor.split(",")[:-1])
            if valor.endswith(".00") or valor.endswith(",00"):
                valor = valor[:-3]
            if valor.endswith(".0") or valor.endswith(",0"):
                valor = valor[:-2]
            if valor.count(" ") == 1:
                valor = valor.split(" ")[0]
            if valor.count(".") == 1 and len(valor.split(".")[1]) == 3:
                valor = valor.replace(".","")
            if valor.count(".") == 1 and len(valor.split(".")[1]) != 3:
                valor = valor.split(".")[0]
            valor = ''.join(re.findall(r'\d+', valor))
            if valor == "":
                valor = "-1"
            try:
                valor_float = float(valor)

                if valor_float >1000000 and index > 795:
                    print ()
                df.loc[index, columna_numerica] = valor_float
            except Exception as e:
                print(e)
        for columna_fecha in valores_fecha:
            fecha = str(row["fecha_factura"]).replace(" ", "")
            try:
                for key, value in diccionario_meses.items():
                    fecha = fecha.upper().replace(key, value)
                if index==200:
                    print ()
                fecha = ''.join(re.findall(r'\d+|/+|-+', fecha))
                fecha_convertida = parser.parse(fecha)
                df.loc[index, columna_fecha] = fecha_convertida

            except Exception as e:
                try:
                    if len(fecha) == 8:
                        fecha_otro_formato = f"{fecha[:2]}/{fecha[2:4]}/{fecha[-4:]}"
                        fecha_convertida = parser.parse(fecha_otro_formato)
                        df.loc[index, columna_fecha] = fecha_convertida
                    else:
                        df.loc[index, columna_fecha] = None
                except Exception as e:
                    df.loc[index, columna_fecha] = None
    for columna_numerica in valores_numericos:
        df[columna_numerica] =  df[columna_numerica].astype(float)
    for columna_fecha in valores_fecha:

        df[columna_fecha] = pd.to_datetime(df[columna_fecha], errors = 'coerce')

    #df.to_excel(f"Salida/{version_lectura}/normalizacion_numericos.xlsx", index=None)
    return df

#ruta_archivo = "Salida/18/lectura_nanonets_lectura_json.xlsx"
#df = pd.read_excel(ruta_archivo, index_col=None)
#procesar(df)
