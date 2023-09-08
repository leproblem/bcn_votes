from fastapi import FastAPI
from typing import Union

from orm_file import ORM


api = FastAPI()
orm = ORM()


@api.post("/add_vote")
def add_vote(voter_id: int, ballot: int):
    response = orm.insert_vote(voter_id, ballot)
    match response['status-code']:
        case 200:
            return {"status": "Success!"}
        case 400:
            return {"status": f"Error! {response['error-msg']}"}