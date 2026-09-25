import logging
from sqlalchemy.orm import Session
from dto.RubrosDTO import RubrosListSP
from exceptions import PruebaNotFoundError
from sqlalchemy import and_, or_, text

def listar_rubros_sp(year: str, db: Session) -> list[RubrosListSP]:
    try:
        rubros_sp = db.execute(
            text("""
                SELECT * FROM rubros_list(:v_year)
            """), 
            {
                'v_year': year
            }
        ).fetchall()

        rubros = [
                    RubrosListSP(
                        rubro_id=row[0],
                        rubro=row[1],
                        short_rubro=row[2],
                        activity_id=row[3],
                        activity_code=row[4],
                        activity_description=row[5]
                    )
                    for row in rubros_sp
                ]

        return rubros
    except Exception as e:
            logging.error(f"Failed to fetch rubros: {str(e)}")
            raise PruebaNotFoundError(str(e))
