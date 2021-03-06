import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi_utils.tasks import repeat_every

from routes.customers import router as customer_router
from routes.settlements import router as settlement_router
from routes.bank_accounts import router as bank_account_router
from routes.sources import router as source_router 
from routes.payments import router as payments_router
from routes.subscriptions import router as subscriptions_router
from routes.ach_debits import router as achdebits_router
from routes.mandates import router as mandate_router
from routes.events_status import router as events_router
from routes.perdix import router as perdix_router
from routes.token import router as token_router
from routes.settings import router as settings_router
from routes.perdix import pending_mandate_status 
from routes.physical_mandate import router as physical_mandate_router
from routes.lotuspay_events import router as lotuspay_event_router
from data.database import get_database, sqlalchemy_engine
from data.customer_model import (customer_metadata)
from data.bankaccount_model import (bankaccount_metadata)
from data.source_model import source_metadata, perdix_metadata
from data.subscription_model import (subscription_metadata)
from data.achdebit_model import (achdebit_metadata)
from data.mandate_model import (mandate_metadata)
from data.events_model import (events_metadata)
from data.logs_model import (logs_metadata)
from data.token_model import (token_metadata)
from data.settings_model import (settings_metadata)
from data.payments_model import (payment_metadata)
from commons import get_env_or_fail


origins = ["*"]


app = FastAPI(title="Perdix-LotusPay",
              debug=True,
    description='testing the descrption',
    version="0.0.1",
    terms_of_service="http://dvara.com/terms/",
    contact={
        "name": "Lotus Pay Integration",
        "url": "http://x-force.example.com/contact/",
        "email": "contact@dvara.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },)


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SCHEDULER_TIME = 'scheduler-time'

scheduler_start_in_seconds = get_env_or_fail(SCHEDULER_TIME, 'start-seconds', SCHEDULER_TIME + ' start-seconds not configured')
scheduler_end_in_seconds = get_env_or_fail(SCHEDULER_TIME, 'end-seconds', SCHEDULER_TIME + ' end-seconds not configured')


@app.on_event("startup")
async def startup():
    await get_database().connect()
    # metadata.create_all(sqlalchemy_engine)
    customer_metadata.create_all(sqlalchemy_engine)
    bankaccount_metadata.create_all(sqlalchemy_engine)
    source_metadata.create_all(sqlalchemy_engine)
    perdix_metadata.create_all(sqlalchemy_engine)
    subscription_metadata.create_all(sqlalchemy_engine)
    logs_metadata.create_all(sqlalchemy_engine)
    achdebit_metadata.create_all(sqlalchemy_engine)
    mandate_metadata.create_all(sqlalchemy_engine)
    events_metadata.create_all(sqlalchemy_engine)
    settings_metadata.create_all(sqlalchemy_engine)
    payment_metadata.create_all(sqlalchemy_engine)
    token_metadata.create_all(sqlalchemy_engine)


@app.on_event("startup")
@repeat_every(seconds=int(scheduler_start_in_seconds) * int(scheduler_end_in_seconds))  # 1 minute
async def update_mandate_task() -> str:
    update_mandate_status = await pending_mandate_status('fake-super-secret-token')
    print("Hello World every 5 minutes")
    return "Hello World"


@app.on_event("shutdown")
async def shutdown():
    await get_database().disconnect()

app.include_router(customer_router, prefix="")
app.include_router(bank_account_router, prefix="/bank-account")
app.include_router(perdix_router, prefix="")
app.include_router(source_router, prefix="")
app.include_router(subscriptions_router, prefix="")
app.include_router(achdebits_router, prefix="")
app.include_router(mandate_router, prefix="")
app.include_router(events_router, prefix="")
app.include_router(lotuspay_event_router, prefix="")
app.include_router(settings_router, prefix="")
app.include_router(payments_router, prefix="")
app.include_router(settlement_router, prefix="")
app.include_router(physical_mandate_router, prefix="")
app.include_router(token_router, prefix="")




if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
