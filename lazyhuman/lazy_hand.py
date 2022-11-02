import pandas as pd
from re import findall as find
from lazyhuman.config_viewp import pandas_start
from lazyhuman.lazytools import LazyTools

class LazyHand():
    def __init__(self,path:str):
        self.path = path
        self.data = self.openDocument(self.path)
        self.data = self.formatear_orden(self.data)
        self.data = self.formatear_fecha(self.data)
        self.data = self.formatear_tipo_envio(self.data)
        self.data = self.formatear_cliente(self.data)
        self.data = self.filtros(self.data)
        self.data = self.formatear_sub_cliente(self.data)
        self.data = self.formato_salida(self.data)

    def openDocument(self, path:str):
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
        data = pd.read_excel(path,names=name_cols, usecols=uses_cols, skiprows=(1,2), dtype=types_cols)

        #agremos una nueva columna al documento
        data = data.assign(tipo='pendiente')

        #ordenamos las columnas
        data = data[['orden','fecha','cliente','tipo','descripcion','cantidad','sub_cliente']]

        return data

    def filtros(self, data:pd.DataFrame) -> pd.DataFrame:
        '''Se realiza un filtrado de los diferentes elementos
            que no se desean dentro del documento final
        '''
        data = data[data.sub_cliente.notnull()] #sub_cliente vacios
        data = data[data.sub_cliente != '980'] #elimina los items de fletes
        data = data[data.sub_cliente != '908'] #elimina los items de concreto
        data = data[data.sub_cliente != '982'] #elimina los items de servicios por distancia

        return data

    def formato_salida(self, data:pd.DataFrame) -> pd.DataFrame:
        data = data.set_index('orden')
        return data

    def formatear_orden(self, document:pd.DataFrame) -> pd.DataFrame:
        '''Obtenemos y ordenamos las Ordenes de Compras de los diferentes registro.''' 
        pattern = r'\d{5}'
        for i, row in document.iterrows():
            if len(find(pattern,str(row.orden))) == 1:
                orden = ''.join(find(pattern,str(row.orden)))
            else:
                document.at[i,'orden'] = orden
        return document

    def formatear_fecha(self, document:pd.DataFrame) -> pd.DataFrame:
        '''Obtenemos todas las fechas de las ordenes de compra''' 
        pattern = r'\d{4}-\d{2}-\d{2}'
        for i, row in document.iterrows():
            if len(find(pattern,str(row.cliente))) == 1:
                fecha = ''.join(find(pattern,str(row.cliente)))
                document.at[i,'fecha'] = fecha
            else:
                document.at[i,'fecha'] = fecha
        return document

    def formatear_tipo_envio(self, data:pd.DataFrame) -> pd.DataFrame:
        '''Para realizar este formateo, buscaremos todos los registros que 
            tengan el codigo del flete 9800001 para relizar el replazo'''
        
        #buscamos todos los registro con el codigo 9800001 y hacemos un listado con las mismas.
        ordenes = [str(row.orden) for i, row in data.iterrows() if data.at[i,'cliente'] == '9800001']

        #realizamos la sustitucion
        for i, row in data.iterrows():
            if str(row.orden) in ordenes:
                data.at[i,'tipo'] = 'FLETE'
            else:
                data.at[i,'tipo'] = 'PROPIA'
        return data

    def formatear_cliente(self, document:pd.DataFrame) -> pd.DataFrame:
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

    def formatear_sub_cliente(self, data:pd.DataFrame) -> pd.DataFrame:
        ''''Realizar la asignacion de los nombres a los cliente'''
        #Filtramos por cliente = CONSUMIDOR
        pattern = r'[A-Z]+'
        ordenes = [row.orden 
                    for _, row in data.iterrows() if row.descripcion == 'PO Number:' and row.cliente == 'CONSUMIDOR FINAL SPS']
        clientes = {row.orden: LazyTools.clean_pattern(pattern,row.sub_cliente)
                    for _, row in data.iterrows() if row.descripcion == 'PO Number:'}

        for i, row in data.iterrows():
            if row.orden in ordenes:
                data.at[i,'cliente'] = clientes[row.orden]
        data = data[data.cantidad.notnull()]
        return data 

    def guardar(self, pathout) -> None:
        filename = self.path.split('/')[-1].split('.')[0]
        pathout = pathout.replace(filename,'').split('.')[0]
        filename = filename.replace(' ','')
        pathout = f"{pathout}{filename}_out.xlsx"
        self.data.to_excel(pathout)
