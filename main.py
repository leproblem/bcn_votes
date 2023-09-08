from api_file import api
from orm_file import ORM
import uvicorn




def main():
    uvicorn.run(api, host="127.0.0.1", port=8000)



"""
При запуске кода, вылетает ошибка, связанная с отсутствием базы локально. 
В идеале создать sqlite базу в этом архиве
"""



if __name__ == "__main__":
    ORM = ORM()
    ORM.create_engine()
    ORM.set_db_session()
    main()