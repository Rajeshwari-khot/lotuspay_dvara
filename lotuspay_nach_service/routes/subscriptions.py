from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from datetime import datetime
from databases import Database
from data.database import get_database, sqlalchemy_engine, insert_logs
from gateway.lotuspay_subscriptions import lotus_pay_post_subscriptions, lotus_pay_subscription_cancel
from data.subscription_model import (
    SubscriptionBase,
    subscriptions,
    SubscriptionCreate,
    SubscriptionDB,
    subscriptions_cancel
)

router = APIRouter()


async def get_subscription_or_404(
    mandate: str, database: Database = Depends(get_database)
) -> SubscriptionDB:
    select_query = subscriptions.select().where(subscriptions.c.mandate == mandate)
    raw_subscription = await database.fetch_one(select_query)

    if raw_subscription is None:
        return None

    return SubscriptionDB(**raw_subscription)


@router.post("/subscription/", response_model=SubscriptionDB, status_code=status.HTTP_201_CREATED,  tags=["Subscriptions"])
async def create_subscription(
    subscription: SubscriptionCreate, database: Database = Depends(get_database)
) -> SubscriptionDB:

    try:
        print("....................coming inside subscription")
        subscription_info = subscription.dict()
        print(f"......coming inside source info..{subscription_info}")
        mandate = subscription_info.get('mandate')
        verify_subscription_in_db = await get_subscription_or_404(mandate, database)
        print(f"------verify_subscription_in_db-----------{verify_subscription_in_db}")
        if verify_subscription_in_db is None:
            response_subscription_id = await lotus_pay_post_subscriptions('subscriptions', subscription_info)
            if response_subscription_id is not None:
                store_record_time = datetime.now()
                subscription_info = {
                    **subscription.dict(),
                    'subscription_id': response_subscription_id,
                    'created_date': store_record_time
                }
                insert_query = subscriptions.insert().values(subscription_info)
                subscription_id = await database.execute(insert_query)
                result = JSONResponse(status_code=200, content={"Customer_id": response_subscription_id})
            else:
                log_id = await insert_logs('MYSQL', 'DB', 'NA', '400', 'problem with lotuspay parameters',
                                           datetime.now())
                result = JSONResponse(status_code=400, content={"message": 'problem with lotuspay parameters'})
        else:
            log_id = await insert_logs('MYSQL', 'DB', 'NA', '200', 'Mandate Already Exists in DB',
                                       datetime.now())
            result = JSONResponse(status_code=200, content={"message": "Mandate Already Exists in DB"})
    except Exception as e:
        log_id = await insert_logs('MYSQL', 'DB', 'NA', '500', 'Error Occurred at DB level',
                                   datetime.now())
        result = JSONResponse(status_code=500, content={"message": f"Error Occurred at DB level - {e.args[0]}"})
    return result


@router.post("/subscription-cancellation", status_code=status.HTTP_200_OK,  tags=["Subscriptions"])
async def create_ach_debits_cancellation(
    subscription: str, database: Database = Depends(get_database)
) -> SubscriptionDB:

    try:
        response_subscription_id = await lotus_pay_subscription_cancel('subscriptions', subscription)
        store_record_time = datetime.now()
        if response_subscription_id is not None:
            subscription_info = {
                'subscription_id': response_subscription_id,
                'created_date': store_record_time
            }
            delete_query = subscriptions_cancel.insert().values(subscription_info)
            subscription_id = await database.execute(delete_query)
        else:
            log_id = await insert_logs('MYSQL', 'DB', 'NA', '400', 'problem with lotuspay parameters',
                                       datetime.now())
            result = JSONResponse(status_code=400, content={"message": 'problem with lotuspay parameters'})
        result = response_subscription_id

    except Exception as e:
        log_id = await insert_logs('MYSQL', 'DB', 'NA', '500', 'Error Occurred at DB level',
                                   datetime.now())
        result = JSONResponse(status_code=500, content={"message": f"Error Occurred at DB level - {e.args[0]}"})
    return result