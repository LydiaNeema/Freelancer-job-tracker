from sqlalchemy import Column,Integer,String,ForeignKey,Text,Float,DateTime,Boolean,func
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime


class Customer(Base):
    __tablename__ = "customers"
class Invoice(Base):
    __tablename__ = "invoices"
class Payment(Base): 
    __tablename__ = "payments"       
