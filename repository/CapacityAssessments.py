import logging
from sqlalchemy.orm import Session
from entity.capacity_assessments import CapacityAssessments
from exceptions import PruebaCreationError, PruebaNotFoundError
from sqlalchemy import text, bindparam, Integer
from dto.CapacityAssessmentsDTO import CapacityAssessmentListSP
from sqlalchemy.dialects.postgresql import ARRAY


def listar(db: Session) -> list[CapacityAssessments]:
    try:
        return db.query(CapacityAssessments).order_by(CapacityAssessments.name.asc()).all()
    except Exception as e:
        logging.error(f"Failed to list CapacityAssessments: {str(e)}")
        raise PruebaNotFoundError(str(e))


def crear(capacidad: CapacityAssessments, db: Session) -> CapacityAssessments:
    try:
        db.add(capacidad)
        db.commit()
        db.refresh(capacidad)
        return capacidad
    except Exception as e:
        db.rollback()
        logging.error(f"Failed to create CapacityAssessments: {str(e)}")
        raise PruebaCreationError(str(e))
def obtener_por_id(id: int, db: Session) -> CapacityAssessments | None:
    try:
        return db.query(CapacityAssessments).filter(CapacityAssessments.id == id).first()
    except Exception as e:
        logging.error(f"Failed to get CapacityAssessments by id: {str(e)}")
        raise PruebaNotFoundError(str(e))
    
def obtener_por_nombre(nombre: str, db: Session) -> CapacityAssessments | bool:
    try:
        return db.query(CapacityAssessments).filter(CapacityAssessments.name.ilike(nombre.strip())).first()
    except Exception as e:
        logging.error(f"Failed to get CapacityAssessments by name: {str(e)}")
        return False
      #  raise PruebaNotFoundError(str(e))
    


def obtener_por_guid(guid: str, db: Session) -> CapacityAssessments | None:
    try:
        return db.query(CapacityAssessments).filter(CapacityAssessments.guid == guid).first()
    except Exception as e:
        logging.error(f"Failed to get CapacityAssessments by guid: {str(e)}")
        raise PruebaNotFoundError(str(e))



def listar_capacity_assessments_por_usuario_sp(
    guid_usuario_msft: str,
    db: Session,
    page: int = 1,
    estado: list[int] = [-1],
    filtro: str = "",
    programa: int = -1,
) -> list[CapacityAssessmentListSP]:
    try:
        query = text("""
    SELECT sp.*, p.first_name, p.other_name, p.last_name, p.other_last_name
    FROM list_capacity_assesstment(
        :guid_usuario_msft, :page, :v_status, :filtro, :v_program
    ) sp
    LEFT JOIN persons p ON p.id = sp.persons_id
""").bindparams(
    bindparam('v_status', type_=ARRAY(Integer))
)

        result = db.execute(
            query,
            {
                'guid_usuario_msft': guid_usuario_msft,
                'page': page,
                'v_status': estado,
                'filtro': filtro,
                'v_program': programa,
            }
        ).fetchall()

        return [
            CapacityAssessmentListSP(
                guid=row[0],                              # guid
                name=row[1],                               # name
                observation=row[2],                        # observation
                approximate_value=row[3],                  # approximate_value
                implementer_id=row[4],                      # implementer_id
                implementer_name=row[5],                    # implementer_name
                policy_approval_date=row[6],                # policy_approval_date
                document_signature_date=row[7],             # document_signature_date
                start_date=row[8],                          # start_date
                end_date=row[9],                            # end_date
                codigo=row[10],                             # code
                program_id=row[11],                         # program_id
                program_name=row[12],                       # program_name
                pid_id=row[13],                             # pid_id
                pad_name=row[14],                           # pad_name
                persons_id=row[15],                         # persons_id
                persons_name=" ".join(x for x in [row[28], row[29], row[30], row[31]] if x), 
                #persons_email=row[16],                      # persons_email
                capacity_assessments_states_id=row[17],     # capacity_assessments_states_id
                modality_id=row[18],                        # modality_id
                modality_name=row[19],                      # modality_name
                pending_my_approval=row[20],                # pending_my_approval
                capacity_assessments_id=row[21],            # capacity_assestments_id (typo en la función SQL)
                approval_request_id=row[22],                # approval_request_id
                user_id=row[23],                            # user_id
                guid_msft=row[24],                          # guid_msft
                step_order_actual_request=row[25],          # step_order_actual_request
                guid_msft_adjustment=row[26],               # guid_msft_adjustment
                total_records=row[27],                      # total_records

            )
            for row in result
        ]
    except Exception as e:
        logging.error(f"Failed to fetch capacity assessments: {str(e)}")
        raise PruebaNotFoundError(str(e))
