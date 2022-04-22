
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from datetime import datetime

from databases import Database
from data.database import get_database, sqlalchemy_engine, insert_logs
from gateway.lotuspay_ach_debit import lotus_pay_achdebit_post, lotus_pay_achdebit_cancel
from data.achdebit_model import (
    achdebits,
    achdebits_cancel,
    ACHDebitBase,
    ACHDebitCreate,
    ACHDebitDB,
)


router = APIRouter()


@router.post("/achdebits", response_model=ACHDebitDB, status_code=status.HTTP_201_CREATED,  tags=["ACH Debits"])
async def create_ach_debits(
    achdebit: ACHDebitCreate, database: Database = Depends(get_database)
) -> ACHDebitDB:

    try:
        achdebit_info = achdebit.dict()
        response_achdebit_id = await lotus_pay_achdebit_post('ach_debits', achdebit_info)
        if response_achdebit_id is not None:
            achdebit_info = {
                **achdebit_info,
                'achdebit_id': response_achdebit_id,
                'created_date': datetime.now()
            }
            insert_query = achdebits.insert().values(achdebit_info)
            achdebit_id = await database.execute(insert_query)
            result = JSONResponse(status_code=200, content={"achdebit_id": response_achdebit_id})

        else:
            log_id = await insert_logs('MYSQL', 'DB', 'NA', '400', 'problem with lotuspay parameters',
                                       datetime.now())
            result = JSONResponse(status_code=400, content={"message": 'problem with lotuspay parameters'})

    except Exception as e:
        log_id = await insert_logs('MYSQL', 'DB', 'NA', '500', 'Error Occurred at DB level',
                                   datetime.now())
        result = JSONResponse(status_code=500, content={"message": f"Error Occurred at DB level - {e.args[0]}"})
    return result


@router.post("/achdebits-cancellation", status_code=status.HTTP_200_OK,  tags=["ACH Debits"])
async def create_ach_debits_cancellation(
    debit_id: str, database: Database = Depends(get_database)
) -> ACHDebitDB:

    try:
        response_achdebit_id = await lotus_pay_achdebit_cancel('ach_debits', debit_id)
        store_record_time = datetime.now()
        if response_achdebit_id is not None:
            subscription_info = {
                'achdebit_id': response_achdebit_id,
                'created_date': store_record_time
            }
            delete_query = achdebits_cancel.insert().values(subscription_info)
            achdebit_id = await database.execute(delete_query)
        else:
            log_id = await insert_logs('MYSQL', 'DB', 'NA', '400', 'problem with lotuspay parameters',
                                       datetime.now())
            result = JSONResponse(status_code=400, content={"message": 'problem with lotuspay parameters'})

        result = response_achdebit_id

    except Exception as e:
        log_id = await insert_logs('MYSQL', 'DB', 'NA', '500', 'Error Occurred at DB level',
                                   datetime.now())
        result = JSONResponse(status_code=500, content={"message": f"Error Occurred at DB level - {e.args[0]}"})
    return result