import os
import sqlalchemy
import sqlite3 as sl
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from table import Votes, BC_Votes
from BC_engine import Blockchain, Block
from crypto_engine import encrypt_message, string_to_byte_array
from Crypto.Random import get_random_bytes


Base = declarative_base()
Session = sessionmaker()

BC_Base = declarative_base()
BC_Session = sessionmaker()
blockchain = Blockchain()

con = sl.connect('voting.db') #если нет файлика, то создаёт его

with con:
 con.execute("""
        CREATE TABLE if not exists votes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            voter_id int not null,
            ballot int not null
         );
     """)

bc_transactions = sl.connect('bc_votes.db')
with bc_transactions:
 bc_transactions.execute("""
        CREATE TABLE if not exists bc_votes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ballot_data varchar not null
         );
     """)


# sql = 'INSERT INTO votes (voter_id, ballot) values(?, ?)'
# new_data = [(1, 1)]
# con.executemany(sql, new_data)

with bc_transactions:
    data = bc_transactions.execute("SELECT * FROM bc_votes")
    print(list(data))
    for row in data:
        print(row)

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
        # voters = []
        with self.db_session() as session:
            
            # for i in session.query(Votes.voter_id).filter(Votes.ballot == ballot):
            #     voters.append(i[0])
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


class ORM_bc:

    def __init__(self):
        self.engine = None
        self.db_session = None
        self.key = None

    def create_engine(self):
        load_dotenv('.env')
        # host = os.environ.get("DB_HOST")
        # port = os.environ.get("DB_PORT")
        # user = os.environ.get("DB_PASSWORD")
        # password = os.environ.get("DB_PASSWORD")
        # database_name = os.environ.get("DB_NAME")
        # self.engine = sqlalchemy.create_engine(f'mysql+pymysql://{user}:{password}@{host}:{port}/{database_name}')
        self.key = os.environ.get("BC_KEY")
        self.engine = sqlalchemy.create_engine('sqlite:///bc_votes.db')  # только для sqlite

    def set_db_session(self):
        self.db_session = sessionmaker(bind=self.engine)

    def insert_vote(self, ballot: int):
        # Create a database connection
        engine = self.create_engine()  # Replace with your database connection string

        # Create a session
        Session = sessionmaker(bind=engine)
        session = Session.configure(bind=engine)
        self.set_db_session()
        print(f'ballot is here {ballot}')
        #block calculation here
        block = Block(f"{ballot}", blockchain.get_latest_block().hash)
        blockchain.add_block(block)
        latest_block = blockchain.get_latest_block()
        t = latest_block.timestamp
        t_str = t.strftime('%Y-%m-%d %H:%M:%S.%f')
        print(f'block timestamp {t_str} is here')
        BC_array_to_cipher = [t_str, latest_block.data, latest_block.previous_hash, latest_block.hash]
        BC_data_joined = ','.join(BC_array_to_cipher)
        key = string_to_byte_array(self.key)
        ciphertext_to_append = encrypt_message(key, BC_data_joined)


        with self.db_session() as session:

            try:
                # Create a new Product instance
                new_vote = BC_Votes(ballot_data=ciphertext_to_append)

                # Add the product to the session
                session.add(new_vote)

                # Commit the transaction to the database
                session.commit()

                print(f"New ciphered block {ciphertext_to_append} registered successfully.")
                return {'status-code': 200}
            except Exception as e:
                # Handle any exceptions (e.g., database errors)
                session.rollback()
                print(f"Error: {str(e)}")
                return {'status-code': 400, 'error-msg': str(e)}
            finally:
                # Close the session
                session.close()

    def find_specific_vote(self, ballot_id: int):

        votes = []

        engine = self.create_engine()
        Session = sessionmaker(bind=engine)
        session = Session.configure(bind=engine)
        self.set_db_session()

        with self.db_session() as session:
            try:
                # Create a new Product instance
                for i in session.query(BC_Votes.ballot_data).filter(BC_Votes.id == ballot_id):
                    votes.append(i[0])

                print(f"Requested ciphered block {ballot_id} extracted successfully.")
                return {'status-code': 200, 'data' : votes}
            except Exception as e:
                # Handle any exceptions (e.g., database errors)
                session.rollback()
                print(f"Error: {str(e)}")
                return {'status-code': 400, 'error-msg': str(e)}
            finally:
                # Close the session
                session.close()