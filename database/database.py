from typing import Annotated
from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

""" You can add a DATABASE_URL environment variable to your .env file """
# DATABASE_URL = os.getenv("DATABASE_URL")

""" Or hard code SQLite here """
# DATABASE_URL = "sqlite:///./todosapp.db"

""" Or hard code PostgreSQL here """
DATABASE_URL = os.getenv("DATABASE_URL")

# engine = create_engine(DATABASE_URL, echo=True)
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
DbSession = Annotated[Session, Depends(get_db)]






# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker, declarative_base
# from sqlalchemy.ext.declarative import declarative_base
# from pathlib import Path
# import json
# import os

# # DATABASE_URL = "postgresql://postgres:abcd1234.@localhost:5432/FCDS"
# DATABASE_URL = os.getenv("DATABASE_URL")
# engine = create_engine(DATABASE_URL, echo=True)
# # Create a configured "Session" class
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# # Create a base class for declarative models
# Base = declarative_base()


# file = Path('settings.json').absolute()

# # if not file.exists():
# #     print(f'WARNING: {file} file not found, you cannot continue, please see settings_template.json')
# #     raise Exception('settings.json file not found, you cannot continue, please see settings_template.json')

# with open(file) as fin:
#     settings = json.load(fin)
#     # Define the database URL
#     # DATABASE_URL = "postgresql://postgres:abcd1234.@localhost:5432/FCDS"
#     DATABASE_URL = f"postgresql://{settings.get('database.user')}:{settings.get('database.password')}.@{settings.get('database.host')}/{settings.get('database.database')}"
#     # Create the SQLAlchemy engine
#     engine = create_engine(DATABASE_URL, echo=True)
#     # Create a configured "Session" class
#     SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#     # Create a base class for declarative models
#     Base = declarative_base()


