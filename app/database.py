from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()
Database_url = "sqlite:///./freelancer.db"

engine = create_engine(Database_url,echo=True)
SessionLocal = sessionmaker(bind=engine)




