"""Configuracion para visualizar los datos en la terminal,
    Para el uso de la Libreria de Pandas"""

def pandas_start(pd) -> None:
    options ={
        'display':{
            'max_columns':None,
            'max_colwidth': 25,
            'expand_frame_repr': False,
            'max_rows': 20,
            'precision': 4,
            'show_dimensions': False
        },
        'mode':{
            'chained_assignment': None
        }
    }

    for category, option in options.items():
        for op, value in option.items():
            pd.set_option(f'{category}.{op}',value)

