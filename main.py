import pandas as pd
from config_viewp import pandas_start
from re import findall as find

def clean_pattern(pattern:str, objStr:str) -> str:
    """Creamos una salida limpia para segun el pattern objStr 

    Args:
        pattern (str): pattern de busqueda 
        objStr (str): Elemento string 

    Returns:
        str: resultado_con formado 
    """
    result = ' '.join(find(pattern,objStr)).replace('RC A ','')
    result = result.replace('RC B ','')
    return result

def openDocument(path:str) -> pd.DataFrame:
    '''Abrimos el documento de los pedidos y le damos el formato deseado.'''
    #colunmas a ser usadas del documento
    uses_cols = [0,1,2,3,4,7]

    #nombre de los columnas a utilizar
    name_cols = ['orden','fecha','cliente','descripcion','sub_cliente','cantidad']

    #tipos de datos para las columnas
    types_cols = {
        'orden':str, 'fecha':str,
        'cliente':str, 'descripcion':str,
        'sub_cliente':str, 'cantidad':float
    }

    #nuevo documento dataframe
    document = pd.read_excel(path,names=name_cols, usecols=uses_cols, skiprows=(1,2), dtype=types_cols)

    #agremos una nueva columna al documento
    document = document.assign(tipo='pendiente')

    #ordenamos las columnas
    document = document[['orden','fecha','cliente','tipo','descripcion','cantidad','sub_cliente']]
    
    return document

def filtros(data:pd.DataFrame) -> pd.DataFrame:
    '''Se realiza un filtrado de los diferentes elementos
        que no se desean dentro del documento final
    '''
    data = data[data.sub_cliente.notnull()] #sub_cliente vacios
    data = data[data.sub_cliente != '980'] #elimina los items de fletes
    data = data[data.sub_cliente != '908'] #elimina los items de concreto
    data = data[data.sub_cliente != '982'] #elimina los items de servicios por distancia

    return data

def formato_salida(data:pd.DataFrame) -> pd.DataFrame:
    data = data.set_index('orden')
    return data

def formatear_orden(document:pd.DataFrame) -> pd.DataFrame:
    '''Obtenemos y ordenamos las Ordenes de Compras de los diferentes registro.''' 
    pattern = r'\d{5}'
    for i, row in document.iterrows():
        if len(find(pattern,str(row.orden))) == 1:
            orden = ''.join(find(pattern,str(row.orden)))
        else:
            document.at[i,'orden'] = orden
    return document

def formatear_fecha(document:pd.DataFrame) -> pd.DataFrame:
    '''Obtenemos todas las fechas de las ordenes de compra''' 
    pattern = r'\d{4}-\d{2}-\d{2}'
    for i, row in document.iterrows():
        if len(find(pattern,str(row.cliente))) == 1:
            fecha = ''.join(find(pattern,str(row.cliente)))
            document.at[i,'fecha'] = fecha
        else:
            document.at[i,'fecha'] = fecha
    return document

def formatear_tipo_envio(data:pd.DataFrame) -> pd.DataFrame:
    '''Para realizar este formateo, buscaremos todos los registros que 
        tengan el codigo del flete 9800001 para relizar el replazo'''
    
    #buscamos todos los registro con el codigo 9800001 y hacemos un listado con las mismas.
    ordenes = [str(row.orden) for i, row in data.iterrows() if data.at[i,'tipo'] == 'FLETE']

    #realizamos la sustitucion
    for i, row in data.iterrows():
        if str(row.cliente) in ordenes:
            data.at[i,'tipo'] = 'FLETE'
        else:
            data.at[i,'tipo'] = 'PROPIA'
    return data

def formatear_cliente(document:pd.DataFrame) -> pd.DataFrame:
    ''''Realiza la asignacion de los nombres a los cliente'''
    pattern = r'[A-Za-z]+'
    cliente = str()

    for i, row in document.iterrows():
        if len(find(pattern,str(row.cliente))) >= 1:
            cliente = ' '.join(find(pattern,str(row.cliente)))
            document.at[i,'cliente'] = cliente
        else:
            document.at[i,'cliente'] = cliente
    return document

def formatear_sub_cliente(data:pd.DataFrame) -> pd.DataFrame:
    ''''Realizar la asignacion de los nombres a los cliente'''
    #Filtramos por cliente = CONSUMIDOR
    pattern = r'[A-Z]+'
    ordenes = [row.orden 
                for _, row in data.iterrows() if row.descripcion == 'PO Number:' and row.cliente == 'CONSUMIDOR FINAL SPS']
    clientes = {row.orden: clean_pattern(pattern,row.sub_cliente)
                for _, row in data.iterrows() if row.descripcion == 'PO Number:'}

    for i, row in data.iterrows():
        if row.orden in ordenes:
            data.at[i,'cliente'] = clientes[row.orden]
    data = data[data.cantidad.notnull()]
    return data 


if __name__ == '__main__':
    pandas_start(pd)
    path = '.\DataSet\OpenOrder.xls'
    doc = openDocument(path)
    doc = formatear_orden(doc.copy())
    doc = formatear_fecha(doc.copy())
    doc = formatear_tipo_envio(doc.copy())
    doc = formatear_cliente(doc.copy())
    doc = filtros(doc.copy())
    doc = formatear_sub_cliente(doc.copy())
    doc = formato_salida(doc.copy())
    doc.to_excel('out.xlsx')