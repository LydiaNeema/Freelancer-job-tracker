from app.models import Customer, Invoice, Payment
from app.database import SessionLocal
from tabulate import tabulate
import re


def list_customers(session):
    customers = session.query(Customer).order_by(Customer.id).all()

    if not customers:
        print("⚠️ No customers found.")
        return

    table = []
    for c in customers:
        # Defensive checks in case of incomplete data
        customer_id = c.id or "❓"
        name = c.name or "❓"
        email = c.email or "❓"
        table.append([customer_id, name, email])

    print(tabulate(table, headers=["ID", "Name", "Email"], tablefmt="fancy_grid"))



def list_invoices(session):
    invoices = session.query(Invoice).all()
    if not invoices:
        print("⚠️ No invoices found.")
        return
    table = []
    for i in invoices:
        if i.customer is None:
            customer_name = "❌ Missing"
        else:
            customer_name = i.customer.name
        table.append([i.id, i.description, i.amount, customer_name])
    print(tabulate(table, headers=["ID", "Description", "Amount", "Customer"], tablefmt="fancy_grid"))



def list_payments(session):
    payments = session.query(Payment).all()
    if not payments:
        print("⚠️ No payments found.")
        return
    table = []
    for p in payments:
        if p.invoice is None:
            invoice_desc = "❌ Missing"
            customer_name = "❌ Missing"
        else:
            invoice_desc = p.invoice.description
            customer_name = p.invoice.customer.name
        table.append([p.id, p.amount, invoice_desc, customer_name])
    print(tabulate(table, headers=["ID", "Amount", "Invoice", "Customer"], tablefmt="fancy_grid"))
    


def show_balances(session):
    customers = session.query(Customer).all()
    if not customers:
        print("⚠️ No customers found.")
        return
    table = []
    for customer in customers:
        total_invoices = sum(inv.amount for inv in customer.invoices)
        total_payments = sum(p.amount for inv in customer.invoices for p in inv.payments)
        balance = total_invoices - total_payments
        table.append([customer.name, f"{balance:.2f}"])
    print(tabulate(table, headers=["Customer", "Balance"], tablefmt="fancy_grid"))
def is_valid_name(name):
    return name and not name.isdigit()
def is_valid_email(email):
    # Basic email validation using regex
    email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(email_regex, email) is not None

def add_customer(session):
    name = input("Enter customer name: ").strip()
    email = input("Enter customer email: ").strip()
    if not is_valid_name(name):
        print("⚠️ Invalid name. Name must be a non-numeric string.")
        return

    if not is_valid_email(email):
        print("⚠️ Invalid email format.")
        return
    new_customer = Customer(name=name, email=email)
    session.add(new_customer)
    session.commit()
    print("✅ Customer added successfully.")


def add_invoice(session):
    list_customers(session)
    try:
        customer_id = int(input("Enter customer ID for the invoice: "))
    except ValueError:
        print("⚠️ Invalid input. Customer ID must be a number.")
        return
    customer = session.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        print("⚠️ Customer not found.")
        return
    description = input("Enter invoice description: ").strip()
    try:
        amount = float(input("Enter invoice amount: "))
    except ValueError:
        print("⚠️ Invalid input. Amount must be a number.")
        return
    new_invoice = Invoice(description=description or "No description", amount=amount, customer_id=customer_id)
    session.add(new_invoice)
    session.commit()
    print("✅ Invoice added successfully.")


def add_payment(session):
    list_invoices(session)
    try:
        invoice_id = int(input("Enter invoice ID for the payment: "))
    except ValueError:
        print("⚠️ Invalid input. Invoice ID must be a number.")
        return
    invoice = session.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not invoice:
        print("⚠️ Invoice not found.")
        return
    try:
        amount = float(input("Enter payment amount: "))
    except ValueError:
        print("⚠️ Invalid input. Amount must be a number.")
        return
    new_payment = Payment(amount=amount, invoice_id=invoice_id)
    session.add(new_payment)
    session.commit()
    print("✅ Payment added successfully.")


def update_customer(session):
    list_customers(session)
    try:
        customer_id = int(input("Enter customer ID to update: "))
    except ValueError:
        print("⚠️ Invalid Customer ID.")
        return
    customer = session.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        print("⚠️ Customer not found.")
        return
    new_name = input(f"Enter new name (current: {customer.name}): ").strip() or customer.name
    new_email = input(f"Enter new email (current: {customer.email}): ").strip() or customer.email
    customer.name = new_name
    customer.email = new_email
    session.commit()
    print("✅ Customer updated successfully.")


def update_invoice(session):
    list_invoices(session)
    try:
        invoice_id = int(input("Enter invoice ID to update: "))
    except ValueError:
        print("⚠️ Invalid Invoice ID.")
        return
    invoice = session.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not invoice:
        print("⚠️ Invoice not found.")
        return
    new_description = input(f"Enter new description (current: {invoice.description}): ").strip() or invoice.description
    new_amount = input(f"Enter new amount (current: {invoice.amount}): ").strip()
    if new_amount:
        try:
            invoice.amount = float(new_amount)
        except ValueError:
            print("⚠️ Invalid input. Amount must be a number.")
            return
    invoice.description = new_description
    session.commit()
    print("✅ Invoice updated successfully.")


def update_payment(session):
    list_payments(session)
    try:
        payment_id = int(input("Enter payment ID to update: "))
    except ValueError:
        print("⚠️ Invalid Payment ID.")
        return
    payment = session.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        print("⚠️ Payment not found.")
        return
    new_amount = input(f"Enter new amount (current: {payment.amount}): ").strip()
    if new_amount:
        try:
            payment.amount = float(new_amount)
        except ValueError:
            print("⚠️ Invalid input. Amount must be a number.")
            return
    session.commit()
    print("✅ Payment updated successfully.")


def delete_customer(session):
    list_customers(session)
    try:
        customer_id = int(input("Enter customer ID to delete: "))
    except ValueError:
        print("⚠️ Invalid input. Please enter a number.")
        return
    customer = session.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        print("⚠️ Customer not found.")
        return
    session.delete(customer)
    session.commit()
    print("✅ Customer deleted successfully.")


def delete_invoice(session):
    list_invoices(session)
    try:
        invoice_id = int(input("Enter Invoice ID to delete: "))
    except ValueError:
        print("⚠️ Invalid input. Please enter a number.")
        return
    invoice = session.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not invoice:
        print("⚠️ Invoice not found.")
        return
    session.delete(invoice)
    session.commit()
    print("✅ Invoice deleted successfully.")


def delete_payment(session):
    list_payments(session)
    try:
        payment_id = int(input("Enter Payment ID to delete: "))
    except ValueError:
        print("⚠️ Invalid input. Please enter a number.")
        return
    payment = session.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        print("⚠️ Payment not found.")
        return
    session.delete(payment)
    session.commit()
    print("✅ Payment deleted successfully.")

def invoice_status_report(session):
    rows = []  
    invoices = session.query(Invoice).all()
    for inv in invoices:
        paid = sum(p.amount for p in inv.payments)
        balance = inv.amount - paid
        status = "Paid" if balance <= 0 else ("Partially Paid" if paid > 0 else "Unpaid")
        rows.append((inv.id, inv.description, f"{inv.amount:.2f}", f"{paid:.2f}", f"{balance:.2f}", status))
    print(tabulate(rows, headers=["ID", "Description", "Amount", "Paid", "Balance", "Status"], tablefmt="fancy_grid"))    


def menu():
    session = SessionLocal()
    while True:
        print("\nFreelancer Management CLI")
        print("-------------------------")
        print("1. List Customers")
        print("2. List Invoices")
        print("3. List Payments")
        print("4. Show Customer Balances")
        print("5. Add Customer")
        print("6. Add Invoice")
        print("7. Add Payment")
        print("8. Update Customer")
        print("9. Update Invoice")
        print("10. Update Payment")
        print("11. Delete Customer")
        print("12. Delete Invoice")
        print("13. Delete Payment")
        print("14. Invoice Status Report")
        print("0. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            list_customers(session)
        elif choice == '2':
            list_invoices(session)
        elif choice == '3':
            list_payments(session)
        elif choice == "4":
            show_balances(session)
        elif choice == "5":
            add_customer(session)
        elif choice == "6":
            add_invoice(session)
        elif choice == "7":
            add_payment(session)
        elif choice == "8":
            update_customer(session)
        elif choice == "9":
            update_invoice(session)
        elif choice == "10":
            update_payment(session)
        elif choice == "11":
            delete_customer(session)
        elif choice == "12":
            delete_invoice(session)
        elif choice == "13":
            delete_payment(session)
        elif choice == "14":
            invoice_status_report(session)    
        elif choice == '0':
            print("👋 Exiting Freelancer Management CLI.")
            break
        else:
            print("⚠️ Invalid choice. Please try again.")

    session.close()


if __name__ == "__main__":
    menu()
