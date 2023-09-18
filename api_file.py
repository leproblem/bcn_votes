from fastapi import FastAPI
from typing import Union

from orm_file import ORM, ORM_bc


api = FastAPI()
orm = ORM()
orm_bc = ORM_bc()


@api.post("/add_vote")
def add_vote(voter_id: int, ballot: int):
    response = orm.insert_vote(voter_id, ballot)
    response_2 = orm_bc.insert_vote(ballot)
    match response['status-code']:
        case 200:
            return {"status": "Success!"}
        case 400:
            return {"status": f"Error! {response['error-msg']}"}