from typing import List, Optional
from pydantic import BaseModel
from dto.ListaGenerica import ListaGenerica

class Listados(BaseModel):
    id_listado: Optional[int]
    tipo_listado: Optional[str]
    lista_generica: Optional[List[ListaGenerica]]
       