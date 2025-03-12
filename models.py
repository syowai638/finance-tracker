from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import date

# ✅ Create a base class for our database models
Base = declarative_base()

# ✅ User Model (Each user has multiple transactions)
class User(Base):
    __tablename__ = 'users'  # Table name in the database

    id = Column(Integer, primary_key=True)  # Unique identifier
    name = Column(String, nullable=False)  # User's name (cannot be empty)
    email = Column(String, unique=True, nullable=False)  # Must be unique

    # Relationship: A user has many transactions
    transactions = relationship("Transaction", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(id={self.id}, name={self.name}, email={self.email})>"

# ✅ Transaction Model (Records income & expenses)
class Transaction(Base):
    __tablename__ = 'transactions'  # Table name in the database

    id = Column(Integer, primary_key=True)  # Unique identifier
    user_id = Column(Integer, ForeignKey('users.id'))  # Links to a user
    amount = Column(Float, nullable=False)  # Can be positive (income) or negative (expense)
    category = Column(String, nullable=False)  # e.g., Food, Transport, Rent
    date = Column(Date, default=date.today)  # Defaults to today's date

    # Relationship: Links transactions to a user
    user = relationship("User", back_populates="transactions")

    def __repr__(self):
        return f"<Transaction(id={self.id}, user_id={self.user_id}, amount={self.amount}, category={self.category}, date={self.date})>"

# ✅ Database Setup
DATABASE_URL = "sqlite:///finance_tracker.db"  # SQLite database file
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# ✅ Create the tables in the database
Base.metadata.create_all(engine)

print("Database setup complete! 🎉")
