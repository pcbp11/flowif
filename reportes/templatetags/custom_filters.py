from django import template

register = template.Library()

@register.filter
def formato_miles(value):
    """
    Formatea un número con puntos como separador de miles.
    """
    try:
        value = int(value)
        return f"{value:,}".replace(",", ".")
    except (ValueError, TypeError):
        return value

@register.filter
def replace_spaces_with_dots(value):
    """
    Reemplaza espacios por puntos en una cadena.
    """
    if isinstance(value, str):
        return value.replace(" ", ".")
    return value
