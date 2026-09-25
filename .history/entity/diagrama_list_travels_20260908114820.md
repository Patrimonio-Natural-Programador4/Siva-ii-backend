```mermaid
flowchart TD
    Start([Inicio: list_travels]) --> P1[Obtener v_id_user desde guid_user_msft]
    P1 --> P2[Obtener v_limit y v_offset para paginación]
    ...
```