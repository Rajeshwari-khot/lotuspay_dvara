
import logging
import json
import pdfkit
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from datetime import datetime
import io
from fpdf import FPDF
from fastapi import FastAPI
from fastapi.responses import FileResponse
from sqlalchemy.sql import text
import aspose.words as aw
import img2pdf
from PIL import Image
from PIL import Image
import os

from databases import Database
import img2pdf

from PIL import Image
import json
from datetime import datetime
from fastapi import APIRouter, Depends, status
import os
import shutil
import ast
from data.database import get_database, sqlalchemy_engine, insert_logs
from fastapi.responses import JSONResponse ,FileResponse
from databases import Database
from fastapi import FastAPI, File,UploadFile,Form
from fastapi import APIRouter, status
from resource.generics import response_to_dict
import requests
from requests import Session, Request
from commons import get_env_or_fail
from requests_toolbelt.multipart.encoder import MultipartEncoder
from data.source_model import (
    sources,
    SourceDB
)

import os
import aspose.words as aw
from data.database import get_database, sqlalchemy_engine, insert_logs
from gateway.lotuspay_source import lotus_pay_post_source, lotus_pay_post_source2, lotus_pay_post_source3, lotus_pay_source_status,lotus_pay_post_source5,lotus_pay_post_sourcewithdraw,lotus_pay_get_sourceprocess
from .events_status import get_event_status
import requests
import base64
from pdfrw import PdfWriter
from fpdf import FPDF
from resource.generics import response_to_dict
from commons import get_env_or_fail
from data.source_model import (
    sources,
    SourceBase,
    SourceCreate,
    SourceDB,
    Source2Create,
    Source3Create,
    Source5Create
)

LOTUSPAY_SERVER = 'lotus-pay-server'
router = APIRouter()

logger = logging.getLogger("arthmate-lender-handoff-service")


async def get_source_or_404(
    source: str,
    database: Database = Depends(get_database)
) -> SourceDB:
    select_query = sources.select().where(sources.c.source_id == source)
    raw_source = await database.fetch_one(select_query)

    if raw_source is None:
        return None

    return SourceDB(**raw_source)


@router.post("/source", status_code=status.HTTP_201_CREATED,  tags=["Sources"])
async def create_source(
    source: SourceCreate,
    database: Database = Depends(get_database)
) -> SourceDB:
    try:
        source_info = source.dict()
        source_id = source_info.get('source_id')
        verify_source_in_db = await get_source_or_404(source_id, database)
        if verify_source_in_db is None:
            response_source_id = await lotus_pay_post_source('sources', source_info)
            if response_source_id is not None:
                get_source_status = await get_event_status(response_source_id)
                source_status = get_source_status['type']
                store_record_time = datetime.now()
                save_source = source_info.get('nach_debit')
                nach_type = source_info.get('type')
                save_source['type'] = nach_type
                save_source['source_status'] = source_status
                save_source['source_id'] = response_source_id
                save_source['created_date'] = store_record_time
                insert_query = sources.insert().values(save_source)
                source_id = await database.execute(insert_query)
                result = JSONResponse(status_code=200, content={"source_id": response_source_id})
            else:
                log_id = await insert_logs('MYSQL', 'DB', 'NA', '400', 'problem with lotuspay parameters',
                                           datetime.now())
                result = JSONResponse(status_code=400, content={"message": 'problem with lotuspay parameters'})
        else:
            print('Source already exists in DB')
            log_id = await insert_logs('MYSQL', 'DB', 'NA', '200', 'Source Already Exists in DB',
                                       datetime.now())
            result = JSONResponse(status_code=200, content={"message": "Source Already Exists in DB"})
    except Exception as e:
        log_id = await insert_logs('MYSQL', 'DB', 'NA', '500', 'Error Occurred at DB level', datetime.now())
        result = JSONResponse(status_code=500, content={"message": f"Error Occurred at DB level - {e.args[0]}"})
    return result



@router.post("/source/{customer_id}", status_code=status.HTTP_201_CREATED,  tags=["Sources"])
async def customer_source(
    source2: Source2Create,
        database: Database = Depends(get_database)
) -> SourceDB:

    try:
        print('Coming inside of Customer')
        source_info = source2.dict()
        source_id = source_info.get('source_id')
        redirect = source_info.get('redirect')
        str_redirect = str(redirect)
        customer = source_info.get('customer')
        verify_source_in_db = await get_source_or_404(source_id, database)
        if verify_source_in_db is None:
            response_source_id = await lotus_pay_post_source2('sources', source_info)
            if response_source_id is not None:
                store_record_time = datetime.now()

                save_source = source_info.get('nach_debit')
                nach_type = source_info.get('type')
                save_source['type'] = nach_type
                save_source['source_id'] = response_source_id
                save_source['created_date'] = store_record_time
                save_source['redirect'] = str_redirect
                save_source['customer'] = customer
                insert_query = sources.insert().values(save_source)
                source_id = await database.execute(insert_query)

                result = JSONResponse(status_code=200, content={"source_id": response_source_id})
            else:
                log_id = await insert_logs('MYSQL', 'DB', 'NA', '400', 'problem with lotuspay parameters',
                                           datetime.now())
                result = JSONResponse(status_code=400, content={"message": 'problem with lotuspay parameters'})

        else:
            print('Source already exists in DB')
            log_id = await insert_logs('MYSQL', 'DB', 'NA', '200', 'Source Already Exists in DB',
                                       datetime.now())
            result = JSONResponse(status_code=200, content={"message": "Source Already Exists in DB"})

    except Exception as e:
        log_id = await insert_logs('MYSQL', 'DB','NA', '500', 'Error Occurred at DB level',
                                   datetime.now())
        result = JSONResponse(status_code=500, content={"message": "Error Occurred at DB level"})

    return result


@router.post("/source/{bank_account}", response_model=SourceDB, status_code=status.HTTP_201_CREATED,  tags=["Sources"])
async def source_bank_account(
    source3: Source3Create,
        database: Database = Depends(get_database)
) -> SourceDB:

    try:
        print('Coming inside of Bank Account')
        source_info = source3.dict()
        print('comingg isndfns')
        print(source_info)
        source_id = source_info.get('bank_account')
        redirect = source_info.get('redirect')
        str_redirect = str(redirect)
        bank_account = source_info.get('bank_account')
        # verify_source_in_db = await get_source_or_404(source_id, database)
        # if verify_source_in_db is None:
        response_source_id = await lotus_pay_post_source3('sources', source_info)
        if response_source_id is not None:
            store_record_time = datetime.now()

            save_source = source_info.get('nach_debit')
            nach_type = source_info.get('type')
            save_source['type'] = nach_type
            save_source['source_id'] = response_source_id
            save_source['created_date'] = store_record_time
            save_source['redirect'] = str_redirect
            save_source['bank_account'] = bank_account
            insert_query = sources.insert().values(save_source)
            source_id = await database.execute(insert_query)

            result = JSONResponse(status_code=200, content={"source_id": response_source_id})
        else:
            log_id = await insert_logs('MYSQL', 'DB', 'NA', '400', 'problem with lotuspay parameters',
                                       datetime.now())
            result = JSONResponse(status_code=400, content={"message": 'problem with lotuspay parameters'})

        # else:
        #     print('Source already exists in DB')
        #     log_id = await insert_logs('MYSQL', 'DB', 'NA', '200', 'Source Already Exists in DB',
        #                                datetime.now())
        #     result = JSONResponse(status_code=200, content={"message": "Source Already Exists in DB"})

    except Exception as e:
        log_id = await insert_logs('MYSQL', 'DB', '500', 'Error Occurred at DB level',
                                   datetime.now())
        result = JSONResponse(status_code=500, content={"message": "Error Occurred at DB level"})

    return result


@router.patch("/source/{source_id}", status_code=status.HTTP_200_OK,  tags=["Sources"])
async def update_source_status(
    source_id: str,
    database: Database = Depends(get_database)
):
    try:

        source_status = await lotus_pay_source_status(source_id)
        if source_status is not None:

            get_source_status = await get_event_status(source_status)
            update_query = sources.select()
            # database.
            testing = await database.execute(update_query)
            print('dkjsafkdjs - ', testing)
            get_mandate_status = get_source_status['type']
            # print('text query', query)
            # source_id = await database.execute(text(query))
            print('printing mandate status from evennts - ', source_status, get_mandate_status)
        # print('coming in main patch request', source_status)

    except Exception as e:
        print(e.args[0])



@router.post("/source5/", response_model=SourceDB, status_code=status.HTTP_201_CREATED,  tags=["Sources"])
async def create_source5(
    source5: Source5Create,
    database: Database = Depends(get_database)) -> SourceDB:
    try:
        print('Coming inside of Customer')
        source_info = source5.dict()
        print(f"---------sourceinfo-----------{source_info}-")
        source_id = source_info.get('source_url')
        print(source_id)
        verify_source_in_db = await get_source_or_404(source_id, database)
        if verify_source_in_db is None:
            response_source_id = await lotus_pay_post_source5('sources', source_info)
            if response_source_id is not None:
                store_record_time = datetime.now()
                nach_debit = source_info.get('nach_debit')
                nach_type = source_info.get('type')
                nach_debit['type'] = nach_type
                nach_debit['source_id'] = response_source_id
                nach_debit['created_date'] = store_record_time
                insert_query = sources.insert().values(nach_debit)
                source_id = await database.execute(insert_query)
                result = JSONResponse(status_code=200, content={
                                      "source_id": response_source_id})
            else:
                log_id = await insert_logs('MYSQL', 'DB',  'NA', '400', 'problem with lotuspay parameters',
                                           datetime.now())
                result = JSONResponse(status_code=400, content={
                                      "message": 'problem with lotuspay parameters'})
        else:
            print('Source already exists in DB')
            log_id = await insert_logs('MYSQL', 'DB', 'NA', '200', 'Source Already Exists in DB',
                                       datetime.now())
            result = JSONResponse(status_code=200, content={
                                  "message": "Source Already Exists in DB"})
        return result
    except Exception as e:
        log_id = await insert_logs('MYSQL', 'DB', 'NA', '500', 'Error Occurred at DB level',
                                   datetime.now())
        result = JSONResponse(status_code=500, content={
                              "message": "Error Occurred at DB level"})
        return result 



# some_file_path="C:\Users\DELL\Downloads\projects\lotuspaydvara-master\lotuspaydvara-master\static"

@router.post("/source-process")
async def upload_file(
    file: UploadFile = File(...), reference1: str = Form(...),  database: Database = Depends(get_database)
):
    validate_url = get_env_or_fail(LOTUSPAY_SERVER, 'base-url', LOTUSPAY_SERVER + ' base-url not configured')
    api_key = get_env_or_fail(LOTUSPAY_SERVER, 'api-key', LOTUSPAY_SERVER + ' api-key not configured')
    url = validate_url + f'/sources/SC0027JSJKQW7U/process'
    headers = {
        'Authorization': 'Basic c2tfdGVzdF81a0NmUHUzV3g2VkJOWnNiYzZhNlRpYlM6'
        }
    file_name = file.filename
    print('filename is ', file, file_name)
    print('-------------FILE',file_name)
    file_path = os.path.abspath(('./static/'))
    print(file_path)
    with open('nature', "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        shutil.copyfile('nature', file_path + '\\' + file_name)
    if not os.path.exists(file_path + 'nature'):
        print('yes there is a file')
        print(file_path)
        os.remove(file_path + '/' + 'nature')
        print("---removed-----")
        shutil.move('nature', file_path)
    else:
        print("------file_path------", file_path)
        print("file is not there")
        shutil.move('nature', file_path)
    with open(file_path + '/' + file_name,"rb") as a_file:
        print('-----------------------------printing file name ', a_file)
        path_proper =  a_file.name
    files=[('file',(file_name,open(path_proper,'rb'),'nature/jpg'))]
    payload={'reference1': reference1}
    response = requests.request("POST", url, headers=headers, data=payload , files=files)
    print(f"------response----{response}")
    print(f"------response.e----{response.encoding}")
    response_context_dict=response.content
    print(f"------response.content----{response_context_dict}")
    # data=json.load(my_json)
    print(type(response_context_dict))
    # dict_str = response_context_dict.decode("UTF-8")
    response_dict=json.loads(response_context_dict.decode('utf-8'))
    return response_dict


@router.post("/source/withdraw", response_model=SourceDB, status_code=status.HTTP_201_CREATED,  tags=["Sources"])
async def source_withdraw(
    source_withdraw: str,
        database: Database = Depends(get_database)
) -> SourceDB:

    try:
        print('Coming inside of source post withdraw')
        source_info = source_withdraw.dict()
        # print('comingg isndfns')
        print(source_info)
        source_id=source_info.get('id')
        # source_id = source_info.get('bank_account')
        # redirect = source_info.get('redirect')
        # str_redirect = str(redirect)
        # bank_account = source_info.get('bank_account')
        # verify_source_in_db = await get_source_or_404(source_id, database)
        # if verify_source_in_db is None:
        response_source_id = await lotus_pay_post_sourcewithdraw('sources', source_info)
        if response_source_id is not None:
            store_record_time = datetime.now()
            save_source={}
            # save_source = source_info.get('nach_debit')
            # nach_type = source_info.get('type')
            # save_source['type'] = nach_type
            save_source['source_withdraw_id'] = response_source_id
            save_source['created_date'] = store_record_time
            # save_source['redirect'] = str_redirect
            # save_source['bank_account'] = bank_account
            insert_query = sources.insert().values(save_source)
            source_id = await database.execute(insert_query)

            result = JSONResponse(status_code=200, content={"source_id": response_source_id})
        else:
            log_id = await insert_logs('MYSQL', 'DB', 'NA', '400', 'problem with lotuspay parameters',
                                       datetime.now())
            result = JSONResponse(status_code=400, content={"message": 'problem with lotuspay parameters'})

        # else:
        #     print('Source already exists in DB')
        #     log_id = await insert_logs('MYSQL', 'DB', 'NA', '200', 'Source Already Exists in DB',
        #                                datetime.now())
        #     result = JSONResponse(status_code=200, content={"message": "Source Already Exists in DB"})

    except Exception as e:
        log_id = await insert_logs('MYSQL', 'DB', '500', 'Error Occurred at DB level',
                                   datetime.now())
        result = JSONResponse(status_code=500, content={"message": "Error Occurred at DB level"})

    return result




@router.get("/lotus-source-pdf",status_code=status.HTTP_200_OK, tags=["Sources"])
async def get_sources_pdf(
    source_id:str
   
):
    print("coming inside source pdf")
    file_path = "C:\\Users\\DELL\\Documents\\lotuspaydvara-master\\lotuspay_nach_service\\static"
    validate_url = get_env_or_fail(LOTUSPAY_SERVER, 'base-url', LOTUSPAY_SERVER + ' base-url not configured')
    api_key = get_env_or_fail(LOTUSPAY_SERVER, 'api-key', LOTUSPAY_SERVER + ' api-key not configured')
    url = validate_url + f'/sources/{source_id}/pdf'
    print(f'----url------{url}')
    source_pdf_response = requests.get(url, auth=(api_key, ''))
    # print('source_response' , type(source_pdf_response))
    result=source_pdf_response.text
    print(source_pdf_response.encoding)
    print(type(result)) # str
    
  
  
    # file = open('C:\\Users\\DELL\\Documents\\lotuspaydvara-master\\lotuspay_nach_service\\static\\tmp.txt', 'rb')
    # byte = file.read()
    # file.close()
    # filepath="C:\\Users\\DELL\\Documents\\lotuspaydvara-master\\lotuspay_nach_service\\static\\hello.jpeg"
    # decodeit = open(filepath, 'wb')
    # res=decodeit.write(base64.b64decode((byte)))
    # decodeit.close()
#     print(res)
#     # return res
   

#  # Creating Image File Object
# ImgFile = open("hello.jpeg","rb")
# # Creating PDF File Object
# PdfFile = open("test1.pdf","wb")
# # Converting Image File to PDF
# PdfFile.write(img2pdf.convert("hello.jpeg"))

# #Closing Image File Object
# ImgFile.close()
# #Closing PDF File Object
# PdfFile.close()


  
# save FPDF() class into
# a variable pdf
# pdf = FPDF()  
  
# # Add a page
# pdf.add_page()
  
# # set style and size of font
# # that you want in the pdf
# pdf.set_font("Arial", size = 15)
 
# # open the text file in read mode
# f = open("C:\\Users\\DELL\\Documents\\lotuspaydvara-master\\lotuspay_nach_service\\static\\tmp.txt", "r")
 
# # insert the texts in pdf
# for x in f:
#     pdf.cell(10000, 1000, txt = x, ln = 1, align = 'C')
  
# # save the pdf with name .pdf
# pdf.output("C:\\Users\\DELL\\Documents\\lotuspaydvara-master\\lotuspay_nach_service\\static\\hello1.pdf")  

 





    print (type(source_pdf_response))
    return FileResponse(path=file_path, filename=file_path)
    # return api_res
  





    