import json
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from datetime import datetime
from databases import Database
from data.database import get_database, sqlalchemy_engine, insert_logs
from gateway.lotuspay_customers import lotuspay_post_customer
import requests
from resource.generics import response_to_dict
from commons import get_env_or_fail
from fastapi import FastAPI, File, Form, UploadFile


LOTUSPAY_SERVER = 'lotus-pay-server'
router = APIRouter()









@router.post("/files/", status_code=status.HTTP_201_CREATED,  tags=["Physical Mandates"])
async def create_physical_mandate(
    file:UploadFile = File(...), reference1: str = Form(...)
):

    validate_url = get_env_or_fail(LOTUSPAY_SERVER, 'base-url', LOTUSPAY_SERVER + ' base-url not configured')
    api_key = get_env_or_fail(LOTUSPAY_SERVER, 'api-key', LOTUSPAY_SERVER + ' api-key not configured')
    url = validate_url + f'/physical_mandate_images/'
    file_response = requests.post(url,files=dict, auth=(api_key, ''))
    file_dict = response_to_dict(file_response)
    
    return {
        "file_size": len(file),
        "token": reference1,
        "fileb_content_type": file.content_type,
    }


@router.get("/physical-mandate-images",status_code=status.HTTP_200_OK, tags=["Physical Mandates"])
async def get_physical_mandate_images(
   
):
    validate_url = get_env_or_fail(LOTUSPAY_SERVER, 'base-url', LOTUSPAY_SERVER + ' base-url not configured')
    api_key = get_env_or_fail(LOTUSPAY_SERVER, 'api-key', LOTUSPAY_SERVER + ' api-key not configured')
    url = validate_url + f'/physical_mandate_images/'
    physical_mandate_response = requests.get(url, auth=(api_key, ''))
    physical_mandate_dict= response_to_dict(physical_mandate_response)
    return physical_mandate_dict   


@router.get("/physical-mandate/images/file",status_code=status.HTTP_200_OK, tags=["Physical Mandates"])
async def get_physical_mandate_file(
   physical_mandate_id:str
):
    validate_url = get_env_or_fail(LOTUSPAY_SERVER, 'base-url', LOTUSPAY_SERVER + ' base-url not configured')
    api_key = get_env_or_fail(LOTUSPAY_SERVER, 'api-key', LOTUSPAY_SERVER + ' api-key not configured')
    url = validate_url + f'/physical_mandate_images/{physical_mandate_id}/file'
    physical_mandate_response = requests.get(url, auth=(api_key, ''))
    print(physical_mandate_response)
    print (type(physical_mandate_response))
    # print(physical_mandate_response.json)
    # nach_dict = response_to_dict(nach_response)
    # source_pdf_dict=physical_mandate_response
    # return source_pdf_dict
    
    # physical_mandate_dict= json.dumps(physical_mandate_response).encode('utf-8')
    # return physical_mandate_dict   


@router.get("/physical-mandate/list",status_code=status.HTTP_200_OK, tags=["Physical Mandates"])
async def get_physical_mandate_list(
   
):
    validate_url = get_env_or_fail(LOTUSPAY_SERVER, 'base-url', LOTUSPAY_SERVER + ' base-url not configured')
    api_key = get_env_or_fail(LOTUSPAY_SERVER, 'api-key', LOTUSPAY_SERVER + ' api-key not configured')
    url = validate_url + f'/physical_mandate_images/'
    physical_mandate_response = requests.get(url, auth=(api_key, ''))
    physical_mandate_dict= response_to_dict(physical_mandate_response)
    return physical_mandate_dict 


