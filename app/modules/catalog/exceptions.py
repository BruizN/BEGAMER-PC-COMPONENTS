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

class BrandNotFoundError(CatalogError):
    """Se lanza cuando no se encuentra la marca"""
    pass

class BrandAlreadyExistsError(CatalogError):
    """Se lanza cuando se intenta crear un duplicado"""
    pass

class BrandNotEmptyError(CatalogError):
    """Se lanza al intentar borrar una marca con productos hijos"""
    pass

class ProductNotFoundError(CatalogError):
    """Se lanza cuando no se encuentra el producto"""
    pass

class ProductAlreadyExistsError(CatalogError):
    """Se lanza cuando se intenta crear un producto duplicado"""
    pass

class ProductNotEmptyError(CatalogError):
    """Se lanza al intentar borrar un producto con variantes hijos"""
    pass

class SkuAlreadyExistsError(CatalogError):
    """Se lanza cuando se intenta crear una variante con un SKU duplicado"""
    pass

class VariantNotFoundError(CatalogError):
    """Se lanza cuando no se encuentra la variante"""
    pass

class VariantNotEmptyError(CatalogError):
    """Se lanza al intentar borrar una variante asociada a ordenes"""
    pass
