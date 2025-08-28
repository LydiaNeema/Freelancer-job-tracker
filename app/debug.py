#!/usr/bin/env python3
from app.models import Customer, Invoice, Payment
from app.database import SessionLocal
# Create a new database session
session = SessionLocal()
# Query and print all customers, invoices, and payments
print("=== Customers ===")
for customer in session.query(Customer).all():
    print(customer.id, customer.name, customer.email)

print("\n=== Invoices ===")
for invoice in session.query(Invoice).all():
    print(
        invoice.id,
        invoice.description,
        invoice.amount,
        f"Customer: {invoice.customer.name}"
    )

print("\n=== Payments ===")
for payment in session.query(Payment).all():
    print(
        payment.id,
        payment.amount,
        f"Invoice: {payment.invoice.description} (Customer: {payment.invoice.customer.name})"
    )

session.close()




