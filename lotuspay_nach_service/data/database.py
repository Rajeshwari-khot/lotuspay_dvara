import sqlalchemy
from databases import Database
from data.logs_model import applogs



DATABASE_URL = "mysql+pymysql://rajeshwari:rajeshwari@database-2.cekazfzvpdz3.us-east-2.rds.amazonaws.com/sys"
database = Database(DATABASE_URL)
sqlalchemy_engine = sqlalchemy.create_engine(DATABASE_URL)


def get_database() -> Database:
    return database


async def insert_logs(url, app_type, request_json, status_code, content, created):
    Database = get_database()
    log_info = {'request': url,
                'request_type': 'POST',
                'app_type': app_type,
                'request_json': request_json,
                'response_status': status_code,
                'response_content': content,
                'created_date': created}
    insert_query = applogs.insert().values(log_info)
    log_id = await Database.execute(insert_query)
    return log_id
