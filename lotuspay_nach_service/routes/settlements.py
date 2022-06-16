from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from datetime import datetime

from databases import Database 
import requests
from resource.generics import response_to_dict
from commons import get_env_or_fail
from data.database import get_database, sqlalchemy_engine, insert_logs

LOTUSPAY_SERVER = 'lotus-pay-server'
router = APIRouter()


@router.get("/settlements",status_code=status.HTTP_200_OK, tags=["Settlements"])
async def get_settlements(
    settlement_id:str
):
    validate_url = get_env_or_fail(LOTUSPAY_SERVER, 'base-url', LOTUSPAY_SERVER + ' base-url not configured')
    api_key = get_env_or_fail(LOTUSPAY_SERVER, 'api-key', LOTUSPAY_SERVER + ' api-key not configured')
    url = validate_url + f'/settlements/{settlement_id}'
    settlement_response = requests.get(url, auth=(api_key, ''))
    settlement_dict = response_to_dict(settlement_response)
    return settlement_dict   


@router.get("/settlements-list",status_code=status.HTTP_200_OK, tags=["Settlements"])
async def get_settlements_list(
    limit:int
):
    validate_url = get_env_or_fail(LOTUSPAY_SERVER, 'base-url', LOTUSPAY_SERVER + ' base-url not configured')
    api_key = get_env_or_fail(LOTUSPAY_SERVER, 'api-key', LOTUSPAY_SERVER + ' api-key not configured')
    url = validate_url + f'/settlements?limit=10'
    settlement_response = requests.get(url, auth=(api_key, ''))
    settlement_dict = response_to_dict(settlement_response)
    return settlement_dict 
