import logging
from sqlalchemy.orm import Session
from entity.contracts import Contracts
from exceptions import PruebaCreationError, PruebaNotFoundError
from sqlalchemy import text
from dto.ContractsDTO import ContractListSP


def listar(db: Session) -> list[Contracts]:
    try:
        return db.query(Contracts).order_by(Contracts.id.desc()).all()
    except Exception as e:
        logging.error(f"Failed to list Contracts: {str(e)}")
        raise PruebaNotFoundError(str(e))


def crear(contrato: Contracts, db: Session) -> Contracts:
    try:
        db.add(contrato)
        db.commit()
        db.refresh(contrato)
        return contrato
    except Exception as e:
        db.rollback()
        logging.error(f"Failed to create Contracts: {str(e)}")
        raise PruebaCreationError(str(e))


def obtener_por_id(id: int, db: Session) -> Contracts | None:
    try:
        return db.query(Contracts).filter(Contracts.id == id).first()
    except Exception as e:
        logging.error(f"Failed to get Contracts by id: {str(e)}")
        raise PruebaNotFoundError(str(e))


def obtener_por_codigo(codigo: str, db: Session) -> Contracts | bool:
    try:
        return db.query(Contracts).filter(Contracts.code.ilike(codigo.strip())).first()
    except Exception as e:
        logging.error(f"Failed to get Contracts by code: {str(e)}")
        return False


def actualizar(contrato: Contracts, db: Session) -> Contracts:
    try:
        db.commit()
        db.refresh(contrato)
        return contrato
    except Exception as e:
        db.rollback()
        logging.error(f"Failed to update Contracts: {str(e)}")
        raise PruebaCreationError(str(e))


def eliminar(contrato: Contracts, db: Session) -> bool:
    try:
        db.delete(contrato)
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        logging.error(f"Failed to delete Contracts: {str(e)}")
        raise PruebaCreationError(str(e))



def listar_contracts_sp(
    db: Session,
    page: int = 1,
    filtro: str = "",
    anio: int = -1,
    tipo: int = -1,
    contrato_padre: int = -1,
) -> list[ContractListSP]:
    try:
        query = text("""
    SELECT sp.*
    FROM list_contracts(
        :page, :filtro, :v_year, :v_type, :v_parent_id
    ) sp
""")

        result = db.execute(
            query,
            {
                'page': page,
                'filtro': filtro,
                'v_year': anio,
                'v_type': tipo,
                'v_parent_id': contrato_padre,
            }
        ).fetchall()

        return [
            ContractListSP(
                id=row[0],                                  # id
                code=row[1],                                # code
                description=row[2],                         # description
                line_paa=row[3],                            # line_paa
                line_pad=row[4],                            # line_pad
                year=row[5],                                # year
                start_contract_date=row[6],                 # start_contract_date
                end_contract_date=row[7],                   # end_contract_date
                bank_code=row[8],                           # bank_code
                address_line_1=row[9],                      # address_line_1
                address_line_2=row[10],                     # address_line_2
                mobile_phone=row[11],                       # mobile_phone
                program_name=row[12],                       # program_name
                is_currency_usd=row[13],                    # is_currency_usd
                contract_type_name=row[14],                 # contract_type_name
                pillar_name=row[15],                        # pillar_name
                expense_category_name=row[16],              # expense_category_name
                purchase_type_name=row[17],                 # purchase_type_name
                observations=row[18],                       # observations
                created_at=row[19],                         # created_at
                updated_at=row[20],                         # updated_at
                policy_approval=row[21],                    # policy_approval
                policy_date=row[22],                        # policy_date
                final_date=row[23],                         # final_date
                early_settlement_date=row[24],              # early_settlement_date
                causes_early_termination=row[25],           # causes_early_termination
                released_resource=row[26],                  # released_resource
                value=row[27],                              # value
                total_adition=row[28],                      # total_adition
                last_dibursement=row[29],                   # last_dibursement
                dibursement_value=row[30],                  # dibursement_value
                accumulated_value=row[31],                  # accumulated_value
                settle_value=row[32],                       # settle_value
                remaining_value=row[33],                    # remaining_value
                total_restante=row[34],                     # total_restante
                can_delete=row[35],                         # can_delete
                grand_released_resource=row[36],            # grand_released_resource
                grand_value=row[37],                        # grand_value
                grand_total_adition=row[38],                # grand_total_adition
                grand_dibursement_value=row[39],            # grand_dibursement_value
                grand_accumulated_value=row[40],            # grand_accumulated_value
                grand_settle_value=row[41],                 # grand_settle_value
                grand_remaining_value=row[42],              # grand_remaining_value
                grand_total_restante=row[43],               # grand_total_restante
                total_records=row[44],                      # total_records
                page_released_resource=row[45],             # page_released_resource
                page_value=row[46],                         # page_value
                page_total_adition=row[47],                 # page_total_adition
                page_dibursement_value=row[48],             # page_dibursement_value
                page_accumulated_value=row[49],             # page_accumulated_value
                page_settle_value=row[50],                  # page_settle_value
                page_remaining_value=row[51],               # page_remaining_value
                page_total_restante=row[52],                # page_total_restante
            )
            for row in result
        ]
    except Exception as e:
        logging.error(f"Failed to fetch contracts: {str(e)}")
        raise PruebaNotFoundError(str(e))