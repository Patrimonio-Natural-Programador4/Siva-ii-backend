from fastapi import HTTPException

class PruebaError(HTTPException):
    """Base exception for prueba-related errors"""
    pass

class PruebaNotFoundError(PruebaError):
    def __init__(self, prueba_id=None):
        message = "Todo not found" if prueba_id is None else f"Todo with id {prueba_id} not found"
        super().__init__(status_code=404, detail=message)

class PruebaCreationError(PruebaError):
    def __init__(self, error: str):
        super().__init__(status_code=500, detail=f"Failed to create prueba: {error}")
