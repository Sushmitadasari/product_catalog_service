from src.uow.sql_uow import SQLUnitOfWork

def get_uow() -> SQLUnitOfWork:
    return SQLUnitOfWork()
