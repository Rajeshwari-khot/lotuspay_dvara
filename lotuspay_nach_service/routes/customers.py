
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from datetime import datetime
from databases import Database
from data.database import get_database, sqlalchemy_engine, insert_logs
from gateway.lotuspay_customers import lotuspay_post_customer
import requests
from resource.generics import response_to_dict
from commons import get_env_or_fail
from data.customer_model import (
    customers,
    CustomerBase,
    CustomerDB,
    CustomerCreate,
)

LOTUSPAY_SERVER = 'lotus-pay-server'
router = APIRouter()


async def get_customer_or_404(
    pan: str, database: Database = Depends(get_database)
) -> CustomerDB:
    select_query = customers.select().where(customers.c.pan == pan)
    raw_customer = await database.fetch_one(select_query)

    if raw_customer is None:
        return None

    return CustomerDB(**raw_customer)


@router.post("/customer", response_model=CustomerDB, status_code=status.HTTP_201_CREATED,  tags=["Customers"])
async def create_customer(
    customer: CustomerCreate, database: Database = Depends(get_database)
) -> CustomerDB:

    try:
        cust_info = customer.dict()
        pan_no = cust_info.get('pan')
        verify_pan_in_db = await get_customer_or_404(pan_no, database)
        if verify_pan_in_db is None:
            response_customer_id = await lotuspay_post_customer('customers', cust_info)
            if response_customer_id is not None:
                store_record_time = datetime.now()
                customer_info = {
                    **customer.dict(),
                    'customer_id': response_customer_id,
                    'created_date': store_record_time
                }
                insert_query = customers.insert().values(customer_info)
                customer_id = await database.execute(insert_query)
                result = JSONResponse(status_code=200, content={"Customer_id": response_customer_id})
            else:
                log_id = await insert_logs('MYSQL', 'DB', 'NA', '400', 'problem with lotuspay parameters',
                                           datetime.now())
                result = JSONResponse(status_code=400, content={"message": 'problem with lotuspay parameters'})
        else:
            log_id = await insert_logs('MYSQL', 'DB', 'NA', '200', 'PAN Already Exists in DB',
                                       datetime.now())
            result = JSONResponse(status_code=200, content={"message": "PAN Already Exists in DB"})
    except Exception as e:
        log_id = await insert_logs('MYSQL', 'DB', 'NA', '500', 'Error Occurred at DB level',
                                   datetime.now())
        result = JSONResponse(status_code=500, content={"message": f"Error Occurred at DB level - {e.args[0]}"})
    return result


@router.get("/customer/test",status_code=status.HTTP_200_OK, tags=["Customers"])
async def get_customer(
    customer_id: str
):
    validate_url = get_env_or_fail(LOTUSPAY_SERVER, 'base-url', LOTUSPAY_SERVER + ' base-url not configured')
    api_key = get_env_or_fail(LOTUSPAY_SERVER, 'api-key', LOTUSPAY_SERVER + ' api-key not configured')
    url = validate_url + f'/customers/{customer_id}'
    customer_response = requests.get(url, auth=(api_key, ''))
    customer_dict = response_to_dict(customer_response)
    return customer_dict   

@router.get("/customer/test1",status_code=status.HTTP_200_OK, tags=["Customers"])
async def get_customer_list(
    limit: int
):
    validate_url = get_env_or_fail(LOTUSPAY_SERVER, 'base-url', LOTUSPAY_SERVER + ' base-url not configured')
    api_key = get_env_or_fail(LOTUSPAY_SERVER, 'api-key', LOTUSPAY_SERVER + ' api-key not configured')
    url = validate_url + f'/customers?limit=5'
    customer_response = requests.get(url, auth=(api_key, ''))
    customer_dict = response_to_dict(customer_response)
    return customer_dict   