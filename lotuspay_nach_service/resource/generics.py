import json


def response_to_dict(response):
    """Converting bytes response to python dictionary"""
    # print("---------------------converting response to dict--------")
    response_content = response.content
    response_decode = response_content.decode("UTF-8")
    json_acceptable_string = response_decode.replace("'", "\"")
    convert_to_json = json.loads(json_acceptable_string)
    response_dict = dict(convert_to_json)
    # print(f"-------response_dict-----------{response_dict}")
    return response_dict
