from datetime import datetime
import requests
from resource.generics import response_to_dict
from fastapi.responses import JSONResponse
from data.database import insert_logs
from commons import get_env_or_fail


LOTUSPAY_SERVER = 'lotus-pay-server'


async def lotus_pay_post_subscriptions(context, data):
    """ Generic Post Method for lotuspay Subscription """
    try:
        print(f"-----data--{data}")
        validate_url = get_env_or_fail(LOTUSPAY_SERVER, 'base-url', LOTUSPAY_SERVER + ' base-url not configured')
        print(f"-----validate_url-----{validate_url}")
        api_key = get_env_or_fail(LOTUSPAY_SERVER, 'api-key', LOTUSPAY_SERVER + ' api-key not configured')
        print(f"-----api_key-----{api_key}")
        url = validate_url + f'/{context}/'
        str_url = str(url)
        str_data = str(data)
        print(f"-----url-----{url}")
        subscription_context_response = requests.post(url, json=data, auth=(api_key, ''))
        print(f"---subscription_context_response----{subscription_context_response.json()}")
        subscription_context_dict = response_to_dict(subscription_context_response)
        subscription_context_response_id = subscription_context_dict.get('id')
        log_id = await insert_logs(str_url, 'LOTUSPAY', str_data, subscription_context_response.status_code, subscription_context_response.content, datetime.now())
        result = subscription_context_response_id

    except Exception as e:
        log_id = await insert_logs(str_url, 'LOTUSPAY', str_data, subscription_context_response.status_code, subscription_context_response.content, datetime.now())
        result = JSONResponse(status_code=500, content={"message": f"Error Occurred at LotusPay Post Method - {e.args[0]}"})

    return result


async def lotus_pay_subscription_cancel(context, subscription_id):
    """ Generic Post Method for lotuspay Subscription """
    try:
        validate_url = get_env_or_fail(LOTUSPAY_SERVER, 'base-url', LOTUSPAY_SERVER + ' base-url not configured')
        api_key = get_env_or_fail(LOTUSPAY_SERVER, 'api-key', LOTUSPAY_SERVER + ' api-key not configured')
        url = validate_url + f'/{context}/{subscription_id}/cancel'
        str_url = str(url)
        subscription_context_response = requests.post(url, auth=(api_key, ''))
        subscription_context_dict = response_to_dict(subscription_context_response)
        subscription_context_id = subscription_context_dict.get('id')
        log_id = await insert_logs(str_url, 'LOTUSPAY', subscription_id, subscription_context_response.status_code, subscription_context_response.content, datetime.now())
        result = subscription_context_id
    except Exception as e:
        log_id = await insert_logs(str_url, 'LOTUSPAY', subscription_id, subscription_context_response.status_code, subscription_context_response.content, datetime.now())
        result = JSONResponse(status_code=500, content={"message": f"Error Occurred at LotusPay Post Method - {e.args[0]}"})

    return result