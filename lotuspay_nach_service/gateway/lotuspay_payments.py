from datetime import datetime
import requests
from resource.generics import response_to_dict
from fastapi.responses import JSONResponse
from data.database import insert_logs


async def lotus_pay_payments_post(context, data):
    """ Generic Post Method for lotuspay payments """
    try:
        url = f'http://api-test.lotuspay.com/v1/{context}/'
        str_url = str(url)
        str_data = str(data)
        print(str_url)
        print(str_data)
        payments_context_response = requests.post(url, data=data, auth=('sk_test_5kCfPu3Wx6VBNZsbc6a6TibS', ''))
        payments_context_dict = response_to_dict(payments_context_response)
        payments_context_response_id = payments_context_dict.get('id')
        log_id = await insert_logs(str_url, 'LOTUSPAY', str_data, payments_context_response.status_code, payments_context_response.content, datetime.now())
        result = payments_context_response_id

    except:
        log_id = await insert_logs(str_url, 'LOTUSPAY', str_data, payments_context_response.status_code, payments_context_response.content, datetime.now())
        result = JSONResponse(status_code=500, content={"message": "Error Occurred at LotusPay Post Method"})

    return result


async def lotus_pay_payments_cancel(context, payment_id):
    """ Generic Post Method for lotuspay payment """
    try:
        url = f'http://api-test.lotuspay.com/v1/{context}/{payment_id}/cancel'
        str_url = str(url)
        
        print(url)
        payments_context_response = requests.post(url, auth=('sk_test_5kCfPu3Wx6VBNZsbc6a6TibS', ''))
        print(payments_context_response.status_code)
        payments_context_dict = response_to_dict(payments_context_response)
        print(payments_context_response.content)
        payments_context_response_id = payments_context_dict.get('id')
        log_id = await insert_logs(str_url, 'LOTUSPAY', payment_id, payments_context_response.status_code, payments_context_response.content, datetime.now())
        result = payments_context_response_id

    except:
        log_id = await insert_logs(str_url, 'LOTUSPAY', payment_id, payments_context_response.status_code, payments_context_response.content, datetime.now())
        result = JSONResponse(status_code=500, content={"message": "Error Occurred at LotusPay Post Method"})

    return result

