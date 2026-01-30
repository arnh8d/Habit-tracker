from sqlalchemy import create_engine, Column, Integer, String, JSON
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

url =("postgresql+psycopg2://"+str(os.getenv('DB_USER'))
      +':'+str(os.getenv('DB_PASS'))+'@'+str(os.getenv('DB_HOST'))+':'
      + str(os.getenv('DB_PORT'))+'/'+str(os.getenv('DB_NAME')) )

engine = create_engine(url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

BASE = declarative_base()

class Habits(BASE):
    __tablename__ = "habits"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    marks = Column(JSON, nullable=False, default= lambda : [])
    streak = Column(Integer, default=0)

