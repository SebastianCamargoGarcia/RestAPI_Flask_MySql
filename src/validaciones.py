# Valida el código (si es numérico y de longitud 6).
def validar_codigo(codigo: str) -> bool:
    return (codigo.isnumeric())

# Valida el nombre (si es un texto sin espacios en blanco de entre 1 y 30 caracteres).
def validar_nombre(nombre: str) -> bool:
    nombre = nombre.strip()
    return (len(nombre) > 0 and len(nombre) <= 30)

# Validar que el rango esté entre 1 y 9.
def validar_rango(rango: int) -> bool:
    rango_texto = str(rango)
    if rango_texto.isnumeric():
        return (rango >= 1 and rango <= 9)
    else:
        return False