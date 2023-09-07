import pandas as pd
from tqdm import tqdm
import difflib
from config import *
def get_categoria(diccionario):
    max_value = max(diccionario, key=diccionario.get)
    return max_value
def match_palabras(descripcion_factura, maestro):
    max_ratio = 0
    producto_max_ratio =""
    for i in maestro:
        if "RINDEMAX" in descripcion_factura:
            print()
        ratio = difflib.SequenceMatcher(None, i, descripcion_factura).ratio()
        if ratio > 0.45 and ratio>max_ratio:
            max_ratio = ratio
            producto_max_ratio = i
        if i in descripcion_factura.split() :
            return i
    if max_ratio != 0:
        return producto_max_ratio

"""
for index_facturas, row_facturas in tqdm(facturas.iterrows(), total= facturas.shape[0]):
    try:
        descripcion_facturas= row_facturas["descripcion"]
        #df[df['ids'].str.contains("ball")]
        for palabra_factura in descripcion_facturas.split(" "):
            if not str(palabra_factura).isnumeric() and len(str(palabra_factura)) > 4:
                categorias_filtradas = categorias[categorias["DescripcionLargaProducto"].str.contains(palabra_factura)]
                for index_categorias, row_categorias in categorias_filtradas.iterrows():
                    descripcion_categorias = row_categorias["DescripcionLargaProducto"]
                    categoria_categorias = row_categorias["SubCategoria"]
                    if palabra_factura in str(descripcion_categorias):
                        if  not palabra_factura in contador_palabras_categorias:
                            contador_palabras_categorias[palabra_factura] = {}
                            contador_palabras_categorias[palabra_factura][categoria_categorias] = 1
                        else:
                            if  not categoria_categorias in contador_palabras_categorias[palabra_factura]:
                                contador_palabras_categorias[palabra_factura][categoria_categorias] = 1
                            else:
                                contador_palabras_categorias[palabra_factura][categoria_categorias] =  contador_palabras_categorias[palabra_factura][categoria_categorias] +1
    except Exception as e:
        print (e)

with open("sample.json", "w") as outfile:
    json.dump(contador_palabras_categorias, outfile)
"""

"""
with open('sample.json') as f:
    data = f.read()

print("Data type before reconstruction : ", type(data))

# reconstructing the data as a dictionary
contador_palabras_categorias = json.loads(data)
categorias_encontradas = []

for index_facturas, row_facturas in tqdm(facturas.iterrows(), total= facturas.shape[0]):
    descripcion_facturas = row_facturas["descripcion"]
    dict_final = {}
    for palabra_factura in descripcion_facturas.split(" "):
        if not str(palabra_factura).isnumeric() and len(str(palabra_factura)) > 4:
            categoria_palabra = get_categoria(contador_palabras_categorias[palabra_factura])
            if not categoria_palabra in dict_final:
                dict_final[categoria_palabra] = 1
            else:
                dict_final[categoria_palabra] = dict_final[categoria_palabra] +1
    categorias_encontradas.append(get_categoria(dict_final))
facturas["Categoria"]
print ()
"""
def procesar(df):
    categorias = pd.read_csv("Categorias.csv", sep=";", encoding="ISO-8859-1")

    categorias = categorias[~pd.isna(categorias["SubCategoria"])]
    categorias = categorias[~pd.isna(categorias["DescripcionLargaProducto"])]
    precios = pd.read_excel("Precio promedio Papel higienico septiembre-octubre 2022.xlsx", index_col=None)
    facturas = df
    contador_palabras_categorias={}
    columna_categorias = []
    subcategorias=[]
    words_list = categorias["DescripcionLargaProducto"].unique().tolist()
    words_list_descripciones_proyecto_ph = precios["Descripciones PH Familia"].unique().tolist()
    words_list_descripciones_maestro_precios = precios["DescripcionLargaProducto (copia)"].unique().tolist()
    math_maestro_precios_descripciones = []
    math_maestro_precios_codigos = []
    for index_facturas, row_facturas in tqdm(facturas.iterrows(), total= facturas.shape[0]):
        #try:

        descripcion_facturas = row_facturas["descripcion"]
        #comparacion_maestro_tr = difflib.get_close_matches(descripcion_facturas,words_list, cutoff = 0.5)
        #comparacion_maestro_papel_higienico_factura = difflib.get_close_matches(str(descripcion_facturas),words_list_descripciones_proyecto_ph)
        descripcion_match_calculada = match_palabras(str(descripcion_facturas), words_list_descripciones_proyecto_ph)
        #comparacion_maestro_papel_higienico_maestro_precios = difflib.get_close_matches(descripcion_facturas,words_list_descripciones_maestro_precios, cutoff = 0.5)
        """
        #a = difflib.get_close_matches(descripcion_facturas, words_list, cutoff=0.05)
        conteo = dict((x,comparacion_maestro_tr.count(x)) for x in set(comparacion_maestro_tr))
        max_value = comparacion_maestro_tr[0]
        precio_factura = row_facturas["precio unit"]
        cantidad_factura = row_facturas["cantidad"]
        codigo_barras = categorias[categorias["DescripcionLargaProducto"] == max_value]["CodigoDeBarras"].tolist()[0]
        categoria = categorias[categorias["DescripcionLargaProducto"] == max_value]["SubCategoria"].tolist()[0]
        subcategoria = categorias[categorias["DescripcionLargaProducto"] == max_value]["Categoria"].tolist()[0]
        subcategorias.append(subcategoria)
        columna_categorias.append(categoria)
        #['PAPEL HIGIENICO SCOTT CUIDADO COMPLETO X 4 UN', 'PAPEL HIGIENICO SCOTT CUIDADO COMPLETO X 4 UN', 'PAPEL HIGIENICO SCOTT CUIDADO COMPLETO X 12 UN']
        print(f"{descripcion_facturas} --> {max_value} --> {categoria} --> {subcategoria}")
    except Exception as e:
        subcategorias.append("No se parece a nada")
        columna_categorias.append("No se parece a nada")
        """
        try:
            if descripcion_match_calculada != None:
                # cb_match = precios[precios["TBLvProductos_CodigoDeBarras"] == codigo_barras]["Precio promedio de venta"].tolist()[0]
                cb_match = precios[precios["Descripciones PH Familia"] == descripcion_match_calculada][
                    "TBLvProductos_CodigoDeBarras"].tolist()[0]
                descripcion_match = precios[precios["Descripciones PH Familia"] == descripcion_match_calculada][
                    "DescripcionLargaProducto (copia)"].tolist()[0]
                math_maestro_precios_descripciones.append(descripcion_match)
                math_maestro_precios_codigos.append(cb_match)
            else:
                math_maestro_precios_descripciones.append("No es de papel higienico")
                math_maestro_precios_codigos.append("No es de papel higienico")
        except Exception as e:
            math_maestro_precios_descripciones.append("No es de papel higienico")
            math_maestro_precios_codigos.append("No es de papel higienico")
    #facturas["SubCategoria"] = columna_categorias
    facturas["descripcionTR"] = math_maestro_precios_descripciones
    facturas["cbTR"] = math_maestro_precios_codigos
    #facturas.to_csv("facturas_modificado_v6.csv", sep =";")
    facturas.to_excel(f"Salida/{version_lectura}/match.xlsx")
    return facturas
def validacion_unidades_valor_igual_a_total(df):
    campos_multiplicacion = ["cantidad", "valor_unitario"]
    total = "total"
    df["validacion unidades x valor unitario igual a total"] = ""
    
    for index, row in df.iterrows():
        try:
            valor1 = float(row[campos_multiplicacion[0]])  # Convertir a número
            valor2 = float(row[campos_multiplicacion[1]])  # Convertir a número
            total_value = float(row[total])  # Convertir a número

            if valor1 * valor2 == total_value:
                df.loc[index, "validacion unidades x valor unitario igual a total"] = 1
            else:
                df.loc[index, "validacion unidades x valor unitario igual a total"] = 0
        except ValueError:
            df.loc[index, "validacion unidades x valor unitario igual a total"] = 0

    return df

def suma_totales_contra_total_factura(data_factura, data_completa, ruta_factura):
    campo_total_linea = "total"
    campo_total_factura = "valor_total_factura"
    
    if campo_total_factura in data_factura.columns:
        total_factura = str(data_factura[campo_total_factura].unique()[0])  # Convertir a cadena
        suma_factura = data_factura[campo_total_linea].astype(str).sum()  # Convertir a cadena antes de la suma
        suma_factura_str = str(suma_factura)  # Convertir a cadena
        a = tuple(data_factura.index.values.tolist())
        data_completa_index = pd.Index(data_factura.index.tolist(), name="foo")
        
        if suma_factura_str == total_factura:  # Comparar cadenas
            data_completa.loc[data_completa["ruta_factura"] == ruta_factura, "Comprobacion_total_linea_igual_a_total_factura"] = 1
        else:
            data_completa.loc[data_completa["ruta_factura"] == ruta_factura, "Comprobacion_total_linea_igual_a_total_factura"] = 0
    else:
        data_completa.loc[data_completa["ruta_factura"] == ruta_factura, "Comprobacion_total_linea_igual_a_total_factura"] = 0

    return data_completa


def limpieza_final(df):
    data_original = validacion_unidades_valor_igual_a_total(df)
    facturas_unicas = data_original["ruta_factura"].unique().tolist()
    df["Comprobacion_total_linea_igual_a_total_factura"] = ""
    for unica in facturas_unicas:
        filter=data_original["ruta_factura"] == unica
        data_factura = data_original[filter]
        data_original = suma_totales_contra_total_factura(data_factura, data_original, unica)

    # data_revisada = pd.read_excel("09-02-2023Match_Solr_New_Model_textos_procesados_match_Tiendas_TR_nuevo_ph_v2.xlsx",
    #                               index_col=None)
    # data_unida = data_original.merge(data_revisada, on="descripcion", how="left")
    #
    # data_unida.loc[data_unida["Tipo"] == 1, "Descricion_tr_nuevo_match_ph"] = "No Encontrado"
    # data_unida.loc[data_unida["Tipo"] == 1, "Codigos_barra_tr_nuevo_match_ph"] = "No Encontrado"
    # data_unida.loc[data_unida["Tipo"] == 1, "Promociones_tr_nuevo_match_ph"] = "No Encontrado"
    #
    # data_eliminada = data_unida[data_unida["Tipo"] != 2]
    #
    # data_eliminada.loc[data_unida["Tipo"] == 3, "Descricion_tr_nuevo_match_ph"] = "Es de PH pero no identifico cual"
    # data_eliminada.loc[data_unida["Tipo"] == 3, "Codigos_barra_tr_nuevo_match_ph"] = "Es de PH pero no identifico cual"
    # data_eliminada.loc[data_unida["Tipo"] == 3, "Promociones_tr_nuevo_match_ph"] = "Es de PH pero no identifico cual"
    ciudad_ruta =[]
    codigo_factura = []
    for index, row in data_original.iterrows():
        img = row["ruta_factura"]
        if 'BARRANQUILLA' in str(img).upper():
            ciudad_ruta.append('BARRANQUILLA')
        elif 'BOGOTÁ' in str(img).upper():
            ciudad_ruta.append('BOGOTA')
        elif 'CALI' in str(img).upper():
            ciudad_ruta.append('CALI')
        elif 'MEDELLÍN' in str(img).upper():
            ciudad_ruta.append('MEDELLIN')
        else:
            ciudad_ruta.append('NO EXTRAIDA')
        codigo_factura.append(img.split("-")[1].split(".")[0])
    data_original["Código factura TR"] = codigo_factura
    data_original["ciudad_verdadera"] = ciudad_ruta
    lista_campos = ["ID", "Código factura TR", "NombreDeProductor", "marca", "distribuidor", "descripcion", "codigoBarra_mailisearch","cantidad", "valor_unitario","iva","iva %","descuento","total",
                    "unidad_medida","subtotal_factura","iva_factura","descuento_factura","valor_total_factura","fecha_factura", "ruta_factura","Bonificacion" ,"detalle_bonificaciones","Departamento",
                    "codigo_producto", "Descricion_tr_nuevo_match_ph","Codigos_barra_tr_nuevo_match_ph", "Promociones_tr_nuevo_match_ph", "Tipo promocion", "Rollo", "PROMOCION",
                    "Detalle Promoción","descripcion_solr","descripcion_mailisearch","Categoria", "SubCategoria", "Nombre Tienda", "Dirección", "Codigo Postal",
                    "Pais", "Departamento", "Municipio", "Zona", "Localidad/Comuna", "Sector", "Barrio", "NSE/Estrato", "Categoría", "Ubicación", "Latitud", "Longitud", "Metros Cuadrados", "Tamaño", "Estado", "Responsable Tienda", "fecha_factura",
                    "Código factura TR", "Cantidad pacas", "Mes factura", "Fecha mes", "Mes de recolección", "Carta",
                    "Link Foto", "Total Pacas sin Iva", "Costo paca sin Iva", "Tipo de producto", "Producto principal",
                    "Categoria regalada", " ", "Producto regalado", "Dinamica", "% Descuento", "Cantidad Regalada",
                    "Costo sin iva unidad regalada", "Precio de lista Cant Regalada",
                    "Costo del rollo con dinamica sin iva", "Rollo con iva",
                    "Precio promedio Sell out producto principal", "Precio promedio total mercado x ciudad",
                    "Mark down", "Mark Up", "Mark Down total mercado", "Mark Up total mercado", "Contribucion",
                    "Rotación", "Rotacion promedio total mercado", "Tiendas vendedoras total mercado",
                    "Contribución x Rotación Total mercado", "valor_total_factura","numero_factura", "validacion unidades x valor unitario igual a total"
                    ,"Comprobacion_total_linea_igual_a_total_factura"]
    for campo in lista_campos:
        if not  campo in data_original.columns:
            data_original[campo] = ''

    data_eliminada = data_original[lista_campos]

    columnas_finales = ["ID", "Código factura TR", "Fabricante", "Marca", "Distribuidor", "Producto", "Código de barras","Cantidad", "Valor unitario monetario linea","Iva monetario linea",
                          "Iva % linea", "Descuento línea","Valor total monetario linea","Unidad de medida", "Subtotal factura", "Iva total factura","Descuento total factura",
                          "Valor total factura","Fecha factura", "Ruta_factura", "Bonificacion","detalle_bonificaciones","Ciudad", "Codigo producto", "Mach ph", "Codigos barra match ph",
                          "Promociones tr match_ph", "Tipo promocion", "Rollo", "Promocion","Detalle Promoción", "Descripcion_solr","descripcion_mailisearch",
                          "Categoria","SubCategoria", "Nombre Tienda", "Dirección", "Codigo Postal",
                          "Pais", "Departamento", "Municipio", "Zona", "Localidad/Comuna", "Sector", "Barrio", "NSE/Estrato", "Categoría", "Ubicación", "Latitud", "Longitud", "Metros Cuadrados", "Tamaño", "Estado", "Responsable Tienda", "fecha_factura",
                        "Código factura TR", "Cantidad pacas", "Mes factura", "Fecha mes", "Mes de recolección",
                        "Carta",
                        "Link Foto", "Total Pacas sin Iva", "Costo paca sin Iva", "Tipo de producto",
                        "Producto principal",
                        "Categoria regalada", " ", "Producto regalado", "Dinamica", "% Descuento", "Cantidad Regalada",
                        "Costo sin iva unidad regalada", "Precio de lista Cant Regalada",
                        "Costo del rollo con dinamica sin iva", "Rollo con iva",
                        "Precio promedio Sell out producto principal", "Precio promedio total mercado x ciudad",
                        "Mark down", "Mark Up", "Mark Down total mercado", "Mark Up total mercado", "Contribucion",
                        "Rotación", "Rotacion promedio total mercado", "Tiendas vendedoras total mercado",
                        "Contribución x Rotación Total mercado", "valor_total_factura", "codigo de factura", "validacion unidades x valor unitario igual a total"
                        ,"Comprobacion_total_linea_igual_a_total_factura"
]
    data_eliminada.columns = columnas_finales

    data_eliminada["codigo de factura"] = data_eliminada["codigo de factura"].replace(replace_codigo_factura)
    data_eliminada["Distribuidor"] = data_eliminada["Distribuidor"].replace(replace_distribuidores)
    data_eliminada["Iva % linea"] = data_eliminada["Iva % linea"].replace(replace_iva_linea)
    #data_eliminada["GUID"] =
    #data_eliminada.to_excel(f"Salida/{version_lectura}/Data_final_consolidada_cortada.xlsx", index=None, encoding= "iso8859-1")
    data_eliminada.to_excel(f"Salida/{version_lectura}/Data_final_consolidada_cortada.xlsx", index=None)

    data_original.to_excel(f"Salida/{version_lectura}/Data_final_consolidada_total.xlsx", index=None)
    print("Proceso terminado con exito")
    return data_eliminada

#df= pd.read_excel(f"Salida/{version_lectura}/data_final_con_dinamicas_total.xlsx")
#limpieza_final(df)