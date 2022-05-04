from datetime import datetime
import email
from operator import itemgetter
import requests
from resource.generics import response_to_dict
from fastapi.responses import JSONResponse
from data.database import insert_logs
from commons import get_env_or_fail


PERDIX_SERVER = 'perdix-server'





async def perdix_post_login(context):
    """ Generic Post Method for perdix login """
    try:
        validate_url = get_env_or_fail(PERDIX_SERVER, 'perdix_base_url', PERDIX_SERVER + ' base-url not configured')
        username = get_env_or_fail(PERDIX_SERVER, 'username', PERDIX_SERVER + ' username not configured')
        password = get_env_or_fail(PERDIX_SERVER, 'password', PERDIX_SERVER + ' password not configured')
        # url = validate_url + f'/{context}/'
        url = validate_url + f'/oauth/token?client_id=application&client_secret=mySecretOAuthSecret&grant_type=password&password={password}&scope=read+write&skip_relogin=yes&username={username}'
        print(url)
        str_url = str(url)
        # str_data = str(data)
        # customer_context_response = requests.post(url, data=data, auth=(api_key, ''))
        login_context_response = requests.post(url)
        print(login_context_response.status_code)
        print(login_context_response.content)
        login_context_dict = response_to_dict(login_context_response)
        print(login_context_dict)
        print(login_context_dict.get('access_token'))
        access_token = login_context_dict.get('access_token')

        # customer_context_response_id = customer_context_dict.get('id')
        # log_id = await insert_logs(str_url, 'LOTUSPAY', str_data, customer_context_response.status_code, customer_context_response.content, datetime.now())
        result = access_token

    except Exception as e:
        print(e.args[0])
        log_id = await insert_logs(str_url, 'LOTUSPAY',login_context_response.status_code, login_context_response.content, datetime.now())
        result = JSONResponse(status_code=500, content={"message": f"Error Occurred at LotusPay Post Method - {e.args[0]}"})

    return result


async def perdix_fetch_customer(customer_id):
    """ Generic Post Method for perdix fetch customer """
    try:
        validate_url = get_env_or_fail(PERDIX_SERVER, 'perdix_base_url', PERDIX_SERVER + ' base-url not configured')
        username = get_env_or_fail(PERDIX_SERVER, 'username', PERDIX_SERVER + ' username not configured')
        password = get_env_or_fail(PERDIX_SERVER, 'password', PERDIX_SERVER + ' password not configured')
        # url = validate_url + f'/{context}/'
        login_token = await perdix_post_login('data')
        print(login_token)
        url = validate_url + f'/api/enrollments/ 238798'
        headers = {
            # "api-key": "aec33b5b9d24c7959623867150691db1fdb574a2bdd2a6e014eb55bee2d0f176",
            # "Group-key": "5369155212050775"
            "Content-Type": "application/json",
            "Content-Length":"0",
            "User-Agent":'My User Agent 1.0',
            "Accept":"*/*",
            "Accept-Encoding":"gzip, deflate, br",
            "Connection":"keep-alive",
            "Authorization": f"bearer {login_token}"
        }
        str_url = str(url)
        print(url)
        
        # str_data = str(data)
        # customer_context_response = requests.post(url, data=data, auth=(api_key, ''))
        customer_context_response = requests.get(url, headers=headers)
        print(customer_context_response.status_code)
        print(customer_context_response.content)
        customer_context_dict = response_to_dict(customer_context_response)
        # print(customer_context_dict)
        # customer_context_response_id = customer_context_dict.get('id')
        # log_id = await insert_logs(str_url, 'LOTUSPAY', str_data, customer_context_response.status_code, customer_context_response.content, datetime.now())
        result = customer_context_dict
        return result

    except Exception as e:
        print(e.args[0])
        log_id = await insert_logs(str_url, 'LOTUSPAY',  customer_context_response.status_code,
                                   customer_context_response.content, datetime.now())
        result = JSONResponse(status_code=500,
                              content={"message": f"Error Occurred at LotusPay Post Method - {e.args[0]}"})

    return result

# async def create_user_data(data):
#     customer_Id=data.get('id','237896')
#     first_name = data.get('firstName', "")
#     middle_name = data.get('middleName', "")
#     last_name = data.get('lastName', "")
#     first_name = (first_name if first_name else "")
#     last_name = (last_name if last_name else "")
#     middle_name = (middle_name if middle_name else "")
#     full_name = first_name + middle_name + last_name
#     email_id = data.get('emailId', "testsm1@gmail.com")
#     email_id = (email_id if email_id else "testsm1@gmail.com")
#     mobile_number = data.get('mobilePhone', "9862590000")
#     # customer_bank_name = .get('customerBankName', "")
#     ifsc_code = data.get('ifscCode', "")
#     account_type = data.get('accountType', 'savings')
#     account_type = (account_type if account_type else "savings")
#     account_number = data.get('accountNumber', "")
#     frequency=data.get('frequency')
   
#     user_data={
#         "customer_Id":customer_Id,
#         "firstName": full_name,
#         "emailId":email_id,
#         "mobilePhone": mobile_number,
#         "accountNumber": account_number,
#         "ifscCode": ifsc_code,
#         "accountType": account_type
    



#     }
#     return user_data