import sys

import pandas as pd
from config import *
import re

def procesar (df):
    try:
        #data = pd.read_excel(f"bonificaciones_2.xlsx", index_col=None)
        data = df
        #productos_regalados = []
        #data = data[["descripcion", "total","ruta_factura"]]
        #cantidad_productos_regalados = []
        palabras_bonificacion_split =["GTS","GTR", "GRTS","GRATIS","+", "GTIS", "GT"]
        #dinamica_arriba = ["BONI", "BONIF"]
        pague_lleve_inicio = ["PG","PAGUE", "PAG"]
        pague_lleve_fin = ["LV","LLEVE", "LLV"]
        #"BONI", "BONIF","LLEVE","OFERTA""OFER","PAG","LLV", "PG","PAGUE","Bonificacion","OFE","OFT","OBSEQUIO"
        detalle_bonificaciones = []
        index_a_borrar = []
        for index,row in data.iterrows():
            try:
                if not index in index_a_borrar:
                    inserte = False
                    for palabra_split in palabras_bonificacion_split:
                        if palabra_split in str(row["descripcion"]):
                            detalle_bonificaciones.append(str(row["descripcion"]).split(palabra_split)[1])
                            inserte = True
                            break
                    if not inserte:
                        encontre_inicio = False
                        encontre_fin = False
                        for inicio in pague_lleve_inicio:
                            if inicio in str(row["descripcion"]):

                                try:
                                    expresion = f"{inicio}[0-9]+"
                                    chars = re.findall(expresion, str(row["descripcion"]))
                                    frase = chars[0]
                                    cantidad_pagada = float(frase.replace(inicio, ""))
                                    encontre_inicio = True
                                    break
                                except:
                                    expresion = f"{inicio} [0-9]+"
                                    chars = re.findall(expresion, str(row["descripcion"]))
                                    frase = chars[0]
                                    cantidad_pagada = float(frase.replace(inicio, ""))
                                    encontre_inicio = True
                                    break

                        for fin in pague_lleve_fin :
                            if fin in str(row["descripcion"]) and encontre_inicio:
                                try:
                                    expresion = f"{fin}[0-9]+"
                                    chars = re.findall(expresion, str(row["descripcion"]))[0]
                                    cantidad_recibida = float(chars.replace(fin, ""))
                                    encontre_fin = True
                                    break
                                except:
                                    expresion = f"{fin} [0-9]+"
                                    chars = re.findall(expresion, str(row["descripcion"]))[0]
                                    cantidad_recibida = float(chars.replace(fin, ""))
                                    encontre_fin = True
                                    break
                        if encontre_inicio and encontre_fin:
                            cantidad_real = cantidad_recibida - cantidad_pagada
                            dinamica = "Bonificacion calculada "+ str(row["descripcion"]).split(inicio)[0] +" X "+ str(cantidad_real)
                            detalle_bonificaciones.append(dinamica)
                        else:
                            if str(row["total"]) in ['0', '0.00', '0.0',0] and not row["total_original"] == -1:
                                insertar = True
                                i = 1
                                index_a_borrar.append(index)
                                dinamica = str(row["descripcion"])
                                while insertar:
                                    if index + i  != data.shape[0] and str(data.loc[index + i, "total"]) in ['0', '0.00', '0.0', '0.008', 0] :
                                        dinamica += " + " + data.loc[index + i, "descripcion"]
                                        index_a_borrar.append(index+i)
                                        i+=1
                                    else:
                                        insertar = False
                                if detalle_bonificaciones[-1] == "No aplica dinamica":
                                    detalle_bonificaciones[-1]= dinamica
                                else:
                                    detalle_bonificaciones[-1] = detalle_bonificaciones[-1] + " + " + dinamica
                            else:
                                detalle_bonificaciones.append("No aplica dinamica")
            except Exception as e:
                detalle_bonificaciones.append("No aplica dinamica")
        data.drop(index_a_borrar, inplace= True)
        data["detalle_bonificaciones"] = detalle_bonificaciones
        data.to_excel(f"Salida/{version_lectura}/data_final_con_dinamicas_total.xlsx", index=None)
        return data
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        print(str(e))
#df= pd.read_excel(f"Salida/{version_lectura}/data_final.xlsx")
#procesar(df)