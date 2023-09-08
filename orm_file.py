import os
import sqlalchemy
import sqlite3 as sl
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from table import Votes

Base = declarative_base()
Session = sessionmaker()

con = sl.connect('voting.db') #если файлика, то создаёт его
with con:
 con.execute("""
        CREATE TABLE if not exists votes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            voter_id int not null,
            ballot int not null
         );
     """)

# sql = 'INSERT INTO votes (voter_id, ballot) values(?, ?)'
# new_data = [(1, 1)]
# con.executemany(sql, new_data)

with con:
    data = con.execute("SELECT * FROM votes")
    print(list(data))
    for row in data:
        print(row)


class ORM:

    def __init__(self):
        self.engine = None
        self.db_session = None

    def create_engine(self):
        # load_dotenv('.env')
        # host = os.environ.get("DB_HOST")
        # port = os.environ.get("DB_PORT")
        # user = os.environ.get("DB_PASSWORD")
        # password = os.environ.get("DB_PASSWORD")
        # database_name = os.environ.get("DB_NAME")
        # self.engine = sqlalchemy.create_engine(f'mysql+pymysql://{user}:{password}@{host}:{port}/{database_name}')
        self.engine = sqlalchemy.create_engine('sqlite:///voting.db') #только для sqlite

    def set_db_session(self):
        self.db_session = sessionmaker(bind=self.engine)

    def find_specific_candidate(self, ballot: int):
        voters = []
        with self.db_session() as session:
            for i in session.query(Votes.voter_id).filter(Votes.ballot == ballot):
                voters.append(i[0])
        return voters

    def insert_vote(self, voter_id:int, ballot:int):
        # Create a database connection
        engine = self.create_engine()  # Replace with your database connection string

        # Create a session
        Session = sessionmaker(bind=engine)
        session = Session.configure(bind=engine)
        self.set_db_session()
        voters = []
        with self.db_session() as session:
            
            for i in session.query(Votes.voter_id).filter(Votes.ballot == ballot):
                voters.append(i[0])
            try:
                # Create a new Product instance
                new_vote = Votes(voter_id=voter_id, ballot=ballot)

                # Add the product to the session
                session.add(new_vote)

                # Commit the transaction to the database
                session.commit()

                print(f"Vote from '{voter_id}', ballot: {ballot} added successfully.")
                return {'status-code': 200}
            except Exception as e:
                # Handle any exceptions (e.g., database errors)
                session.rollback()
                print(f"Error: {str(e)}")
                return {'status-code': 400, 'error-msg': str(e)}
            finally:
                # Close the session
                session.close()