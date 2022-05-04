from fastapi import APIRouter, Depends, status,Body
from fastapi.responses import JSONResponse
from datetime import datetime
from functools import lru_cache
import logging
from requests.exceptions import Timeout
import config
from resource.generics import response_to_dict
from gateway.perdix import perdix_post_login,perdix_fetch_customer
from gateway.lotuspay_source import lotus_pay_post_source5



from data.database import get_database, sqlalchemy_engine, insert_logs

router=APIRouter()


@lru_cache()
def get_settings():
    return config.Settings()






@router.post("/perdix",status_code=status.HTTP_200_OK,  tags=["Perdix"])
async def fetch_customer(customer_id):
    try:
        # test = await perdix_post_login('data')
        result={}
        request_payload={
            "type": "nach_debit"
        }
        test = await perdix_fetch_customer('customer_id')
        # print(customer_id)

        # result = test.get('customerBankAccounts')[0]
        customer_dict=test.get('customerBankAccounts')[0]
        result["debtor_account_name"]=customer_dict.get("customerNameAsInBank")
        result["debtor_agent_mmbid"]=customer_dict.get("ifscCode")
        result["debtor_account_number"]=customer_dict.get("accountNumber")
        result["debtor_account_type"]=customer_dict.get("accountType").lower()

        result["amount_maximum"]=test.get("cbCheckList")[0].get("loanAmount")
        print("---------------------------",type(result["amount_maximum"]))
        result["debtor_email"]=test.get("verifications")[0].get("emailId")
        result["debtor_mobile"]=test.get("verifications")[0].get("mobileNo")
        request_payload["nach_debit"] = result
        # result['amount_maximum']=bank_amount.get('loanAmount')
        print(f"------------request_payload------------{request_payload}")
        source_detail=await lotus_pay_post_source5('sources', result)
        print(f"------------source_detail------------{source_detail}")
        # print(customer_id).
        return source_detail
    except Exception as e:
        print(e.args[0])



# @router.post("/process-perdix-data")
# async def post_perdix_to_user_data(
#         payload: dict = Body(...)
# ):
#     user_info = await create_user_data(payload)
   
#     print(user_info)
# @router.post("/process-automator-data")
# async def post_automator_data(
#         payload: dict = Body(...),
#         settings: config.Settings = Depends(get_settings),
# ):
#     try:

#         # prepare the user data from perdix data
#         user_info = await create_user_data(payload['']['customerBankAccounts'])
#     except Timeout as ex:
#         print(e.args[0])

#     return {"result": "success"}