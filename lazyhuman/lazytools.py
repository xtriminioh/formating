from re import findall as find

class LazyTools:
    def clean_pattern(pattern:str, objstr:str) -> str:
        """Creamos una salida limpia para segun el pattern objStr 

        Args:
            pattern (str): pattern de busqueda 
            objStr (str): Elemento string 

        Returns:
            str: resultado_con formado 
        """
        result = ' '.join(find(pattern,objstr)).replace('RC A ','')
        result = result.replace('RC B ','')
        return result