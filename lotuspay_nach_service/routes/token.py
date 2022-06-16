from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from datetime import datetime
from databases import Database
from data.database import get_database, sqlalchemy_engine, insert_logs
from gateway.lotuspay_token import lotus_pay_post_token
import requests
from resource.generics import response_to_dict
from commons import get_env_or_fail
from data.token_model import (
    tokens,
    TokenBase,
    TokenDB,
    TokenCreate,
    TokenCreate2
)

LOTUSPAY_SERVER = 'lotus-pay-server'
router = APIRouter()







@router.post("/tokenfull", response_model=TokenDB, status_code=status.HTTP_201_CREATED,  tags=["Tokens"])
async def create_token(
    token: TokenCreate, database: Database = Depends(get_database)
)-> TokenDB:
    try:
        token_info = token.dict()
        print('------------------TOKEN', token_info)
        
        
        response_token_id = await lotus_pay_post_token('tokens',  token_info, perdix=True)
        print(f"----response_token_id---{response_token_id}")
        store_record_time = datetime.now()
        if response_token_id is not None:
            type_info = {}
            token_inf = {
                'token_id': response_token_id,
                
                'created_date': store_record_time
            }
            insert_query = tokens.insert().values(token_inf)
            db_token_id = await database.execute(insert_query)
            result = JSONResponse(status_code=200, content={"token_id": response_token_id})
        else:
            log_id = await insert_logs('MYSQL', 'DB', 'NA', '400', 'problem with lotuspay parameters',
                                       datetime.now())
            result = JSONResponse(status_code=500, content={"message": "Error Occurred at LotusPay level"})
    except Exception as e:
        log_id = await insert_logs('MYSQL', 'DB', 'NA', '500', 'Error Occurred at DB level',
                                   datetime.now())
        result = JSONResponse(status_code=500, content={"message": f"Error Occurred at DB level - {e.args[0]}"})
    return result