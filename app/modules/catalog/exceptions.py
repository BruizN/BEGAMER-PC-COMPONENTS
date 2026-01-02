class CatalogError(Exception):
    """Clase base para todos los errores del módulo de catálogo"""
    pass

class CategoryNotFoundError(CatalogError):
    """Se lanza cuando no se encuentra la categoría"""
    pass

class CategoryAlreadyExistsError(CatalogError):
    """Se lanza cuando se intenta crear un duplicado"""
    pass

class CategoryNotEmptyError(CatalogError):
    """Se lanza al intentar borrar una categoría con productos hijos"""
    pass