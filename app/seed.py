from app.models import Customer,Payment,Invoice
from app.database import SessionLocal,engine,Base
from datetime import datetime

Base.metadata.create_all(bind=engine)

session = SessionLocal()

session.query(Customer).delete()
session.query(Invoice).delete()
session.query(Payment).delete()

#creating sample customers
customer1 = Customer(name = "Lydia Neema", email = "lydianeema25@gmail.com")
customer2 = Customer(name = "Bob Smith", email = "bobsmith@gmail.com")
session.add_all([customer1,customer2])
session.commit()

#creating invoices for customer1
invoice1 = Invoice(description = "Web development services", amount = 1500.00, customer_id = customer1.id)
invoice2 = Invoice(description = "Graphic design services", amount = 800.00, customer_id = customer1.id)
session.add_all([invoice1,invoice2])
session.commit()

#creating invoices for customer2
invoice3 = Invoice(description = "SEO services", amount = 600.00, customer_id = customer2.id)
invoice4 = Invoice(description = "Content writing services", amount = 400.00, customer_id = customer2.id)
session.add_all([invoice3,invoice4])
session.commit()


#creating payments for invoices of customer1 and customer2
payment1 = Payment(amount=200.0, invoice_id=invoice1.id)
payment2 = Payment(amount=300.0, invoice_id=invoice1.id)  # Lydia fully paid invoice1
payment3 = Payment(amount=400.0, invoice_id=invoice3.id) 
payment4= Payment(amount =400.0, invoice_id=invoice4.id) # Bob partially paid
session.add_all([payment1, payment2, payment3,payment4]) 
session.commit()
session.close()