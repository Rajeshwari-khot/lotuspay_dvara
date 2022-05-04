from datetime import datetime
import requests
from resource.generics import response_to_dict
from fastapi.responses import JSONResponse
from data.database import get_database, sqlalchemy_engine, insert_logs
from commons import get_env_or_fail


LOTUSPAY_SERVER = 'lotus-pay-server'


async def lotus_pay_post_source(context, data):
    """ Generic Post Method for lotuspay Surces """
    try:
        validate_url = get_env_or_fail(LOTUSPAY_SERVER, 'base-url', LOTUSPAY_SERVER + ' base-url not configured')
        api_key = get_env_or_fail(LOTUSPAY_SERVER, 'api-key', LOTUSPAY_SERVER + ' api-key not configured')
        url = validate_url + f'/{context}/'
        str_url = str(url)
        str_data = str(data)
        source_context_response = requests.post(url, json=data, auth=(api_key, ''))
        source_context_dict = response_to_dict(source_context_response)
        source_context_response_id = source_context_dict.get('id')
       
        log_id = await insert_logs(str_url, 'LOTUSPAY', str_data, source_context_response.status_code, source_context_response.content, datetime.now())

        result = source_context_response_id
      
        

    except Exception as e:
        log_id = await insert_logs(str_url, 'LOTUSPAY', str_data, source_context_response.status_code, source_context_response.content, datetime.now())
        result = JSONResponse(status_code=500, content={"message": f"Error Occurred at LotusPay Post Method - {e.args[0]}"})
    return result

# async def get_source_status(source_id):
#     url='https://api-test.lotuspay.com/v1/events/{source_id}'
#     api_key = get_env_or_fail(LOTUSPAY_SERVER, 'api-key', LOTUSPAY_SERVER + ' api-key not configured')
#     events_response = requests.get(url)
#     print(f"----------EVENTS jSON-------------------{events_response.json()}")
# #    print(events_response.json())
#     return "pending"

# async def get_mandate_status(source_id):
# #    validate_url = get_env_or_fail(LOTUSPAY_SERVER, 'base-url', LOTUSPAY_SERVER + ' base-url not configured')
# #    api_key = get_env_or_fail(LOTUSPAY_SERVER, 'api-key', LOTUSPAY_SERVER + ' api-key not configured')
# #    url = validate_url + f'/{context}/'
# #    str_url = str(url)
#    url='https://api-test.lotuspay.com/v1/events/{mandate_id}'
#    events=requests.get(url)
#    print(events.json())
#    return "got status"


async def lotus_pay_post_source2(context, data):
    """ Generic Post Method for lotuspay Sources """
    try:
        validate_url = get_env_or_fail(LOTUSPAY_SERVER, 'base-url', LOTUSPAY_SERVER + ' base-url not configured')
        api_key = get_env_or_fail(LOTUSPAY_SERVER, 'api-key', LOTUSPAY_SERVER + ' api-key not configured')
        url = validate_url + f'/{context}/'
        str_url = str(url)
        str_data = str(data)
        source_context_response = requests.post(url, json=data, auth=(api_key, ''))
        source_context_dict = response_to_dict(source_context_response)
        source_context_response_id = source_context_dict.get('id')
        log_id = await insert_logs(str_url, 'LOTUSPAY', str_data, source_context_response.status_code, source_context_response.content, datetime.now())

        result = source_context_response_id

    except Exception as e:
        log_id = await insert_logs(str_url, 'LOTUSPAY', str_data, source_context_response.status_code, source_context_response.content, datetime.now())
        result = JSONResponse(status_code=500, content={"message": f"Error Occurred at LotusPay Post Method - {e.args[0]}"})
    return result


async def lotus_pay_post_source3(context, data):
    """ Generic Post Method for lotuspay Sources """
    try:
        url = f'http://api-test.lotuspay.com/v1/{context}'
        str_url = str(url)
        str_data = str(data)
        print('coming inside source3 ', data)
        source_context_response = requests.post(url, json=data, auth=('sk_test_5kCfPu3Wx6VBNZsbc6a6TibS', ''))
        source_context_dict = response_to_dict(source_context_response)
        source_context_response_id = source_context_dict.get('id')
        log_id = await insert_logs(str_url, 'LOTUSPAY', str_data, source_context_response.status_code, source_context_response.content, datetime.now())

        result = source_context_response_id

    except Exception as e:
        log_id = await insert_logs(str_url, 'LOTUSPAY', str_data, source_context_response.status_code, source_context_response.content, datetime.now())
        result = JSONResponse(status_code=500, content={"message": f"Error Occurred at LotusPay Post Method - {e.args[0]}"})
    return result

async def lotus_pay_post_source4(context, data):
    """ Generic Post Method for lotuspay Sources """
    try:
        url = f'http://api-test.lotuspay.com/v1/{context}'
        str_url = str(url)
        str_data = str(data)
        print('coming inside source3 ', data)
        source_context_response = requests.post(url, json=data, auth=('sk_test_5kCfPu3Wx6VBNZsbc6a6TibS', ''))
        source_context_dict = response_to_dict(source_context_response)
        source_context_response_id = source_context_dict.get('id')
        log_id = await insert_logs(str_url, 'LOTUSPAY', str_data, source_context_response.status_code, source_context_response.content, datetime.now())

        result = source_context_response_id

    except Exception as e:
        log_id = await insert_logs(str_url, 'LOTUSPAY', str_data, source_context_response.status_code, source_context_response.content, datetime.now())
        result = JSONResponse(status_code=500, content={"message": f"Error Occurred at LotusPay Post Method - {e.args[0]}"})
    return result

async def lotus_pay_post_source5(context, data):
    """ Generic Post Method for lotuspay Sources """
    try:
        print(f"-------------context-------------{context}")
        print(f"-------------data-------------{data}")
        url = f'https://api-test.lotuspay.com/v1/{context}'
        str_url = str(url)
        str_data = str(data)
        # print('coming inside source5 ', data)
        source_context_response = requests.post(url, json=data, auth=('sk_test_5kCfPu3Wx6VBNZsbc6a6TibS', ''))
        print("-------------source_context_response-------------")
        print(source_context_response.json())
        source_context_dict = response_to_dict(source_context_response)

        print(source_context_dict)
        source_context_response_id = source_context_dict.get('source_id')
        print(f"---------source_context_response_id------{source_context_response_id}")
        log_id = await insert_logs(str_url, 'LOTUSPAY', str_data, source_context_response.status_code, source_context_response.content, datetime.now())

        result = source_context_response_id

    except Exception as e:
        log_id = await insert_logs(str_url, 'LOTUSPAY', str_data, source_context_response.status_code, source_context_response.content, datetime.now())
        result = JSONResponse(status_code=500, content={"message": "Error Occurred at LotusPay Post Method"})
    return result

async def lotus_pay_get_sourceprocess(source_id):
    """ Generic Get Method for lotuspay listing specific source process for a specific customer"""
    
    print(f'in lotus_pay_get_sourceprocess with {source_id}')
    url = f' https://api-test.lotuspay.com/v1/sources/{source_id}/process'
    print(f"url = {url}")
    sourceprocess_context_response = requests.post(url, auth=('sk_test_5kCfPu3Wx6VBNZsbc6a6TibS', ''))
    print(f" -----------------------{sourceprocess_context_response.content}")
    sourceprocess_context_dict = response_to_dict(sourceprocess_context_response)
    result = sourceprocess_context_dict
    return result

async def lotus_pay_get_sourcewithdraw(source_id):
    """ Generic Get Method for lotuspay listing specific source withdraw for a specific customer"""
    
    print(f'in lotus_pay_get_sourcewithdraw with {source_id}')
    url = f' https://api-test.lotuspay.com/v1/sources/{source_id}/withdraw'
    print(f"url = {url}")
    sourcewithdraw_context_response = requests.post(url, auth=('sk_test_5kCfPu3Wx6VBNZsbc6a6TibS', ''))
    print(f" -----------------------{sourcewithdraw_context_response.content}")
    sourcewithdraw_context_dict = response_to_dict(sourcewithdraw_context_response)
    result = sourcewithdraw_context_dict
    return result


async def lotus_pay_source_status(source_id):
    """Generic Get Method for lotuspay listing specific source withdraw for a specific customer"""
    try:
        validate_url = get_env_or_fail(LOTUSPAY_SERVER, 'base-url', LOTUSPAY_SERVER + ' base-url not configured')
        api_key = get_env_or_fail(LOTUSPAY_SERVER, 'api-key', LOTUSPAY_SERVER + ' api-key not configured')
        url = validate_url + f'/sources/{source_id}'
        print(f"-------------{url}")
       
    
        source_context_response=requests.get(url,auth=(api_key, ''))
        print(f"-------------------------------'{source_context_response}")
        source_context_dict=response_to_dict(source_context_response)
        source_context_response_id=source_context_dict.get('mandate')
        result=source_context_response_id
        print(f"---------------{result}")
        return result
    except Exception as e:
        result = JSONResponse(status_code=500, content={"message": "Error Occurred at LotusPay Post Method"})
        return result

