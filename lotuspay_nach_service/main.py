import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Query, status
from routes.customers import router as customer_router
from routes.bank_accounts import router as bank_account_router
from routes.sources import router as source_router
from routes.subscriptions import router as subscriptions_router
from routes.ach_debits import router as achdebits_router
from routes.mandates import router as mandate_router
from routes.events_status import router as events_router
from data.database import get_database, sqlalchemy_engine
from data.customer_model import (customer_metadata)
from data.bankaccount_model import (bankaccount_metadata)
from data.source_model import (source_metadata)
from data.subscription_model import (subscription_metadata)
from data.achdebit_model import (achdebit_metadata)
from data.mandate_model import (mandate_metadata)

from data.logs_model import (logs_metadata)


app = FastAPI(title="Perdix-LotusPay",
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


@app.on_event("startup")
async def startup():
    await get_database().connect()
    # metadata.create_all(sqlalchemy_engine)
    customer_metadata.create_all(sqlalchemy_engine)
    bankaccount_metadata.create_all(sqlalchemy_engine)
    source_metadata.create_all(sqlalchemy_engine)
    subscription_metadata.create_all(sqlalchemy_engine)
    logs_metadata.create_all(sqlalchemy_engine)
    achdebit_metadata.create_all(sqlalchemy_engine)
    mandate_metadata.create_all(sqlalchemy_engine)


@app.on_event("shutdown")
async def shutdown():
    await get_database().disconnect()

app.include_router(customer_router, prefix="")
app.include_router(bank_account_router, prefix="/bank-account")
app.include_router(source_router, prefix="")
app.include_router(subscriptions_router, prefix="")
app.include_router(achdebits_router, prefix="")
app.include_router(mandate_router, prefix="")
app.include_router(events_router, prefix="")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
