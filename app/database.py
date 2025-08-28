from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#create the database connection and session
Base = declarative_base()
Database_url = "sqlite:///./freelancer.db"

engine = create_engine(Database_url,echo=False)
SessionLocal = sessionmaker(bind=engine)




