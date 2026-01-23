"""
cv_utils.py
Utilidades compartidas para el sistema de generación de CV
"""

# Keywords para clasificación de secciones
# Rangos Espaciales (Basados en Objetivo_No_editar.pdf)
# Estructura: (Y_min, Y_max)
LEFT_COL_RANGES = {
    'HEADER': (0, 130),
    'EDUCATION': (130, 315),
    'PAPERS': (315, 409),
    'SKILLS': (409, 710),
    'LANGUAGE': (710, 1000)
}

RIGHT_COL_RANGES = {
    'EXPERIENCE': (0, 80),   # Title only
    'JOBSITY': (80, 145),
    'ZENTA': (145, 215),
    'DEUNA': (215, 365),
    'SPOT': (365, 475),
    'EPAM': (475, 540),
    'WALMART': (540, 670),
    'LAMNGEN': (670, 1000)
}

def classify_element(elem):
    """
    Clasifica un elemento de texto basado en su posición espacial (X, Y).
    
    Args:
        elem (dict): Diccionario con keys 'x', 'y' (y opcionalmente 'text')
        
    Returns:
        str: Nombre de la sección o 'OTHER'
    """
    x = elem.get('x', 0)
    y = elem.get('y', 0)
    
    # Columna Izquierda (X < 200)
    if x < 200:
        for section, (y_min, y_max) in LEFT_COL_RANGES.items():
            if y_min <= y < y_max:
                return section
                
    # Columna Derecha (X >= 200)
    else:
        for section, (y_min, y_max) in RIGHT_COL_RANGES.items():
            if y_min <= y < y_max:
                return section
                
    return 'OTHER'
