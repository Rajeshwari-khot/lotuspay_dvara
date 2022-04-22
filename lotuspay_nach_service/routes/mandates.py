from fastapi import APIRouter, Depends, status, Body
from fastapi.responses import JSONResponse
from datetime import datetime

from databases import Database
from data.database import get_database, sqlalchemy_engine, insert_logs
from gateway.lotuspay_mandate import lotus_pay_patch_mandate, lotus_pay_mandate_cancel


from data.mandate_model import (
    mandates,
    MandateBase,
    MandateDB,
    mandates_cancel,
    MandateCancelCreate
)


router = APIRouter()


@router.post("/mandate", response_model=MandateDB, status_code=status.HTTP_201_CREATED,  tags=["Mandates"])
async def update_mandate(
    id_token: str,
    mandate_id: str,
    payload: dict = Body({"metadata":{"key":"value"}}),
    database: Database = Depends(get_database)
) -> MandateDB:
    try:
        response_mandate_id = await lotus_pay_patch_mandate('mandates', mandate_id, id_token, payload)
        if response_mandate_id is not None:
            store_record_time = datetime.now()
            mandate_info = {
                'mandate_id': mandate_id,
                'metadata': str(payload),
                'created_date': store_record_time
            }
            insert_query = mandates.insert().values(mandate_info)
            mandate_db_id = await database.execute(insert_query)
        result = JSONResponse(status_code=200, content={"mandate_id": mandate_id})
    except Exception as e:
        log_id = await insert_logs('MYSQL', 'DB', 'NA', '500', e.args[0],
                                   datetime.now())
        result = JSONResponse(status_code=500, content={"message": f"Error Occurred at DB level - {e.args[0]}"})
    return result


@router.post("/mandate-cancellation", status_code=status.HTTP_200_OK,  tags=["Mandates"])
async def mandate_cancellation(
        reason: MandateCancelCreate,
        mandate_id: str,
        database: Database = Depends(get_database)
) -> MandateDB:

    try:
        reason_info = reason.dict()
        response_mandate_id = await lotus_pay_mandate_cancel('mandates', mandate_id, reason_info)
        store_record_time = datetime.now()
        if response_mandate_id is not None:
            mandate_info = {
                'mandate_id': response_mandate_id,
                'created_date': store_record_time
            }
            delete_query = mandates_cancel.insert().values(mandate_info)
            db_mandate_id = await database.execute(delete_query)
            result = JSONResponse(status_code=200, content={"Customer_id": mandate_id})
        else:
            log_id = await insert_logs('MYSQL', 'DB', 'NA', '400', 'problem with lotuspay parameters',
                                       datetime.now())
            result = JSONResponse(status_code=500, content={"message": "Error Occurred at LotusPay level"})

    except Exception as e:
        log_id = await insert_logs('MYSQL', 'DB', 'NA', '500', 'Error Occurred at DB level',
                                   datetime.now())
        result = JSONResponse(status_code=500, content={"message": f"Error Occurred at DB level - {e.args[0]}"})
    return result
