from sqlalchemy import create_engine, Column, Integer, String, JSON
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv


load_dotenv()

url =f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

engine = create_engine(url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

BASE = declarative_base()

class Habits(BASE):
    __tablename__ = "habits"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    marks = Column(JSON, nullable=False, default=[])
    streak = Column(Integer, default=0)

