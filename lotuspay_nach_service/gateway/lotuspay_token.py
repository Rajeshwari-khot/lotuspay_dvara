

from datetime import datetime
import requests
from resource.generics import response_to_dict
from fastapi.responses import JSONResponse
from data.database import insert_logs
from commons import get_env_or_fail


LOTUSPAY_SERVER = 'lotus-pay-server'



async def lotus_pay_post_token(context, data, perdix=None):
    """ Generic Post Method for lotuspay Sources """
    try:
        validate_url = get_env_or_fail(LOTUSPAY_SERVER, 'base-url', LOTUSPAY_SERVER + ' base-url not configured')
        api_key = get_env_or_fail(LOTUSPAY_SERVER, 'api-key', LOTUSPAY_SERVER + ' api-key not configured')
        url = validate_url + f'/{context}/'
        str_url = str(url)
        str_data = str(data)
        token_context_response = requests.post(url, json=data, auth=(api_key, ''))
        token_context_dict = response_to_dict(token_context_response)
        
        token_context_response_id = token_context_dict.get('id')

        print(token_context_response.content)
        if perdix:
            result=token_context_dict
        else:
            result = token_context_response_id
        log_id = await insert_logs(str_url, 'LOTUSPAY', str_data, token_context_response.status_code, token_context_response.content, datetime.now())
        result = token_context_response_id
    except Exception as e:
        log_id = await insert_logs(str_url, 'LOTUSPAY', str_data, token_context_response.status_code, token_context_response.content, datetime.now())
        result = JSONResponse(status_code=500, content={"message": f"Error Occurred at LotusPay Post Method - {e.args[0]}"})
    return result