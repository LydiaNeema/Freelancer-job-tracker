#!/usr/bin/env python3
from app.models import Customer,Invoice,Payment
from app.database import Base,engine,SessionLocal

Base.metadata.create_all(bind=engine)
session = SessionLocal()
import ipdb; ipdb.set_trace()




