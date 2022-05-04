
import logging
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from datetime import datetime




from resource.generics import response_to_dict

from databases import Database
from data.database import get_database, sqlalchemy_engine, insert_logs
from gateway.lotuspay_source import lotus_pay_post_source, lotus_pay_post_source2, lotus_pay_post_source3,lotus_pay_get_sourceprocess,lotus_pay_post_source4,lotus_pay_post_source5,lotus_pay_get_sourcewithdraw,lotus_pay_source_status
from .events_status import get_event_status
from data.source_model import (
    sources,
    SourceBase,
    SourceCreate,
    SourceDB,
    Source2Create,
    Source3Create,
    Source4Create,
    Source5Create
)


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
            print(f"------------------------response_source_id---------{response_source_id}")

           
            if response_source_id is not None:
                response_status=await get_event_status(response_source_id)
                print(response_status)
               
                status_source=response_status.get('type')
                print(f"----------status_source-----{status_source}")
               
                
    
                # mandate_status=await get_mandate_status(source_id)
                
                store_record_time = datetime.now()
                save_source = source_info.get('nach_debit')
                nach_type = source_info.get('type')
                # response_status=source_info.get('status')
                save_source['type'] = nach_type
                save_source['source_id'] = response_source_id
                save_source['created_date'] = store_record_time
                save_source['source_status']= status_source
                
                insert_query = sources.insert().values(save_source)
                source_id = await database.execute(insert_query)

                result = JSONResponse(status_code=200, content={"source_id": response_source_id})
            else:
                log_id = await insert_logs('MYSQL', 'DB', 'NA', '400', 'problem with lotuspay parameters',
                                           datetime.now())
                result = JSONResponse(status_code=400, content={"message": 'problem with lotuspay parameters'})

        else:
            print('Source already exists in database')
            log_id = await insert_logs('MYSQL', 'DB', 'NA', '200', 'Source Already Exists  in DB',
                                       datetime.now())
            result = JSONResponse(status_code=200, content={"message": "Source Already Exists in DB"})
        return result

    except Exception as e:
        log_id = await insert_logs('MYSQL', 'DB', 'NA', '500', 'Error Occurred at database level',
                                   datetime.now())
        result = JSONResponse(status_code=500, content={"message": f"Error Occurred at DB level - {e.args[0]}"})

    return result


@router.post("/source/{customer_id}", status_code=status.HTTP_201_CREATED,  tags=["Sources"])
async def customer_source(
    source2: Source2Create,
    database: Database = Depends(get_database)
    ) -> SourceDB:
    try:
        print('this is try')
        source_info = source2.dict()
        print(f"-------source info----{source_info}")
        result = source_info
        source_id = source_info.get('source_id')
        redirect = source_info.get('redirect')
        str_redirect = str(redirect)
        customer = source_info.get('customer')
        verify_source_in_db = await get_source_or_404(source_id, database)
        print(f"--verify_source_in_db---------{verify_source_in_db}--")
        if verify_source_in_db is None:
            print(f"inside if block")
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
                log_id = await insert_logs('MYSQL', 'DB', 'NA', '400', 'problem with lotuspay  parameters',
                                           datetime.now())
                result = JSONResponse(status_code=400, content={"message": 'problem with lotuspay  parameters'})

        else:
            print('Source already exists in DB')
            log_id = await insert_logs('MYSQL', 'DB', 'NA', '200', 'Source Already Exists in DB',
                                       datetime.now())
            result = JSONResponse(status_code=200, content={"message": "Source Already Exists in DB"})

    except Exception as e:
        result = e
        log_id = await insert_logs('MYSQL', 'DB', '500', 'Error Occurred at DB level',
                                   datetime.now())
        result = JSONResponse(status_code=500, content={"message": "Error Occurred at db level"})

    return result


@router.post("/source/test/{bank_account}", response_model=SourceDB, status_code=status.HTTP_201_CREATED,  tags=["Sources"])
async def source_bank_account(
    source3: Source3Create,
        database: Database = Depends(get_database)
) -> SourceDB:

    try:
        print('Coming inside of Bank Account')
        source_info = source3.dict()
        
        print(source_info)
        source_id = source_info.get('bank_account')
        redirect = source_info.get('redirect')
        str_redirect = str(redirect)
        bank_account = source_info.get('bank_account')
        
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

       

    except Exception as e:
        log_id = await insert_logs('MYSQL', 'DB', '500', 'Error Occurred at DB level',
                                   datetime.now())
        result = JSONResponse(status_code=500, content={"message": "Error Occurred at DB level"})

    return result

@router.post("/source/test1/{bank_account_token}", response_model=SourceDB, status_code=status.HTTP_201_CREATED,  tags=["Sources"])
async def source_bank_account4(
    source4: Source4Create,
        database: Database = Depends(get_database)
) -> SourceDB:

    try:
        print('Coming inside of Bank Account')
        source_info = source4.dict()
        
        print(source_info)
        source_id = source_info.get('bank_account')
        redirect = source_info.get('redirect')
        str_redirect = str(redirect)
        bank_account = source_info.get('bank_account')
       
        response_source_id = await lotus_pay_post_source4('sources', source_info)
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
            log_id = await insert_logs('MYSQL', 'DB', 'NA', '400', 'problem with lotuspay level parameters',
                                       datetime.now())
            result = JSONResponse(status_code=400, content={"message": 'problem with lotuspay  parameters'})

        
    except Exception as e:
        log_id = await insert_logs('MYSQL', 'DB', '500', 'Error Occurred at DB level',
                                   datetime.now())
        result = JSONResponse(status_code=500, content={"message": "Error Occurred at DB level"})

    return result

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
                # nach_debit['url']=response_source_url
                nach_debit['created_date'] = store_record_time
                insert_query = sources.insert().values(nach_debit)
                source_url= await database.execute(insert_query)

                result = JSONResponse(status_code=200, content={
                                      "source_url": response_source_id})
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


@router.post("/lotus-sourceprocess/{source_id}", status_code=status.HTTP_200_OK,  tags=["source process"])
async def lotus_get_sourceprocess(source_id, database: Database = Depends(get_database)) -> SourceDB:
    print(f"hello this is source id from path {source_id}")
    test = await lotus_pay_get_sourceprocess(source_id)
    return test


@router.post("/lotus-sourcewithdraw/{source_id}", status_code=status.HTTP_200_OK,  tags=["source withdraw"])
async def lotus_get_sourcewithdraw(source_id, database: Database = Depends(get_database)) -> SourceDB:
    print(f"hello this is source id from path {source_id}")
    test = await lotus_pay_get_sourcewithdraw(source_id)
    return test


@router.patch("/source/{source_id}", status_code=status.HTTP_200_OK,  tags=["Sources"])
async def update_source_status(
    source_id:str,
    database: Database = Depends(get_database)
):
  try:
      mandate_id=await lotus_pay_source_status(source_id)
      print(f"--------source_id----{source_id}")
      print(f"--------------------source status-----{mandate_id}")#mandate_id
      if mandate_id is not None:
        mandate_status=await get_event_status(mandate_id)
        source_status=await get_event_status(source_id)
        print(f"------source_status--------------{source_status}")
        print("--mandate status and source status-------",source_status.get('type'),mandate_status.get('type'))
        
        query = sources.update().values(mandate=mandate_id, mandate_status=mandate_status.get('type'), source_status=source_status.get('type')).where(source_id==source_id)
        source_id = await database.execute(query)
  except Exception as e:
       result = JSONResponse(status_code=500, content={"message": f"Error Occurred at DB level - {e.args[0]}"})




    




