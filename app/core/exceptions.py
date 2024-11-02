class ModelAlreadyRunningException(Exception):
    """Excepción lanzada cuando se intenta iniciar un modelo que ya está en ejecución."""
    pass

class ModelAlreadyStoppedException(Exception):
    """Excepción lanzada cuando se intenta detener un modelo que ya está detenido."""
    pass
