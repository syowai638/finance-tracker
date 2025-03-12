import re
import click
from models import session, User, Transaction, setup_database
from datetime import datetime

# ✅ Ensure the database is initialized before running commands
setup_database()

# ✅ Email Validation Function
def is_valid_email(email):
    """Check if the email is in a valid format."""
    email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(email_pattern, email) is not None

@click.group()
def cli():
    """Finance Tracker CLI - Manage expenses efficiently"""
    pass

# ✅ 0. Create a User
@click.command()
@click.option("--name", prompt="Name", type=str, help="User's full name")
@click.option("--email", prompt="Email", type=str, help="User's email (must be unique)")
def create_user(name, email):
    """Create a new user account with email validation."""
    
    # ✅ Validate email format
    if not is_valid_email(email):
        click.echo("❌ Invalid email format. Please enter a valid email (e.g., name@example.com).")
        return

    try:
        # ✅ Check if the email already exists
        existing_user = session.query(User).filter_by(email=email).first()
        if existing_user:
            click.echo("❌ Error: A user with this email already exists.")
            return

        # ✅ Create new user
        new_user = User(name=name, email=email)
        session.add(new_user)
        session.commit()
        click.echo(f"✅ User '{name}' created successfully! Your User ID is {new_user.id}")

    except Exception as e:
        click.echo(f"❌ Error: {e}")


# ✅ 1. Register a New User
@click.command()
@click.option("--name", prompt="User Name", type=str, help="Name of the new user")
@click.option("--email", prompt="User Email", type=str, help="Email address (must be unique)")
def add_user(name, email):
    """Register a new user"""
    existing_user = session.query(User).filter_by(email=email).first()
    if existing_user:
        click.echo("❌ Email already exists. Please use a different one.")
        return

    user = User(name=name, email=email)
    session.add(user)
    session.commit()
    click.echo(f"✅ User '{name}' has been successfully registered.")

# ✅ 2. Add an Expense
@click.command()
@click.option("--user_id", prompt="User ID", type=int, help="ID of the user making the transaction")
@click.option("--amount", prompt="Amount", type=float, help="Expense amount")
@click.option("--category", prompt="Category", type=str, help="Expense category (e.g., Food, Rent, Transport)")
@click.option("--description", prompt="Description", type=str, help="Short description of the expense")
@click.option("--date", prompt="Date (YYYY-MM-DD)", default=str(datetime.today().date()), help="Date of the transaction")
def add_expense(user_id, amount, category, description, date):
    """Add a new expense"""
    try:
        # Check if the user exists
        user = session.query(User).filter_by(id=user_id).first()
        if not user:
            click.echo("❌ User not found. Please create a user first.")
            return

        # Ensure the amount is valid
        if amount <= 0:
            click.echo("❌ Amount must be greater than zero.")
            return
        
        transaction = Transaction(
            user_id=user_id, 
            amount=amount, 
            category=category, 
            description=description,  # ✅ Added description
            date=datetime.strptime(date, "%Y-%m-%d")
        )
        session.add(transaction)
        session.commit()
        click.echo(f"✅ Expense of {amount} added under '{category}' for User ID {user_id}.")
    except Exception as e:
        click.echo(f"❌ Error: {e}")

# ✅ 3. View Expenses (with filtering options)
@click.command()
@click.option("--user_id", prompt="User ID", type=int, help="User whose expenses you want to view")
@click.option("--category", default=None, help="Filter by category (optional)")
@click.option("--start_date", default=None, help="Filter from a start date (YYYY-MM-DD, optional)")
@click.option("--end_date", default=None, help="Filter up to an end date (YYYY-MM-DD, optional)")
def view_expenses(user_id, category, start_date, end_date):
    """View all expenses, optionally filtered by category or date range"""
    query = session.query(Transaction).filter_by(user_id=user_id)
    
    if category:
        query = query.filter(Transaction.category == category)
    if start_date:
        query = query.filter(Transaction.date >= datetime.strptime(start_date, "%Y-%m-%d"))
    if end_date:
        query = query.filter(Transaction.date <= datetime.strptime(end_date, "%Y-%m-%d"))

    expenses = query.all()
    if not expenses:
        click.echo("❌ No expenses found.")
        return
    
    click.echo("📜 Your Expenses:")
    for exp in expenses:
        click.echo(f"{exp.id}. {exp.date} - {exp.category}: {exp.amount} | {exp.description}")

# ✅ 4. Edit an Expense
@click.command()
@click.option("--expense_id", prompt="Expense ID", type=int, help="ID of the expense to edit")
@click.option("--amount", type=float, help="New amount (leave blank to keep the same)")
@click.option("--category", type=str, help="New category (leave blank to keep the same)")
@click.option("--description", type=str, help="New description (leave blank to keep the same)")
@click.option("--date", type=str, help="New date (YYYY-MM-DD, leave blank to keep the same)")
def edit_expense(expense_id, amount, category, description, date):
    """Edit an existing expense"""
    expense = session.query(Transaction).filter_by(id=expense_id).first()
    
    if not expense:
        click.echo("❌ Expense not found.")
        return

    if amount:
        expense.amount = amount
    if category:
        expense.category = category
    if description:
        expense.description = description
    if date:
        try:
            expense.date = datetime.strptime(date, "%Y-%m-%d").date()
        except ValueError:
            click.echo("❌ Invalid date format. Use YYYY-MM-DD.")
            return

    session.commit()
    click.echo("✅ Expense updated successfully.")


# ✅ 5. Delete an Expense
@click.command()
@click.option("--expense_id", prompt="Expense ID", type=int, help="ID of the expense to delete")
def delete_expense(expense_id):
    """Delete an expense"""
    expense = session.query(Transaction).filter_by(id=expense_id).first()
    if not expense:
        click.echo("❌ Expense not found.")
        return
    
    session.delete(expense)
    session.commit()
    click.echo("✅ Expense deleted.")

# ✅ 6. Generate Reports
@click.command()
@click.option("--user_id", prompt="User ID", type=int, help="User whose report you want to generate")
@click.option("--category", default=None, help="Summarize by category (optional)")
@click.option("--start_date", default=None, help="From date (YYYY-MM-DD, optional)")
@click.option("--end_date", default=None, help="To date (YYYY-MM-DD, optional)")
def generate_report(user_id, category, start_date, end_date):
    """Generate a financial report summarizing expenses"""
    query = session.query(Transaction).filter_by(user_id=user_id)
    
    if category:
        query = query.filter(Transaction.category == category)
    if start_date:
        query = query.filter(Transaction.date >= datetime.strptime(start_date, "%Y-%m-%d"))
    if end_date:
        query = query.filter(Transaction.date <= datetime.strptime(end_date, "%Y-%m-%d"))

    total = sum(exp.amount for exp in query.all())
    click.echo(f"📊 Total Spending: {total}")

# ✅ Register CLI commands
cli.add_command(create_user)  # Add user creation command
cli.add_command(add_user)  # ✅ Added user registration command
cli.add_command(add_expense)
cli.add_command(view_expenses)
cli.add_command(edit_expense)
cli.add_command(delete_expense)
cli.add_command(generate_report)

if __name__ == "__main__":
    cli()
