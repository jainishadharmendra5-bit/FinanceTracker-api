from fastapi import FastAPI
from pydantic import BaseModel
from enum import Enum


app = FastAPI()

@app.get("/")
def home():
    return {"message": "Hello, World!"}

transactions = []
next_id = 1


class Transaction(BaseModel):
    category: str
    amount: float
    type: str
    id: int = None

class TransactionType(str, Enum):
    income = "income"
    expense = "expense"

@app.post("/transactions")
def create_transaction(transaction: Transaction):
    global next_id
    transaction.id = next_id
    next_id += 1
    transactions.append(transaction)
    return {"message": "Transaction created successfully", "transaction": transaction}

@app.get("/transactions")
def get_transactions():
    return transactions


@app.get("/transactions/filter")
def filter_transactions(category: str = None, type: str = None):
    filtered = transactions
    if category is not None:
        filtered = [t for t in filtered if t.category == category]
    if type is not None:
        filtered = [t for t in filtered if t.type == type]
    return filtered



@app.get("/transactions/summary")
def summary():
    total_income = sum(t.amount for t in transactions if t.type == "income")
    total_expense = sum(t.amount for t in transactions if t.type == "expense")
    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "balance": total_income - total_expense
    }

@app.delete("/transactions/{transaction_id}")
def delete_transaction(transaction_id: int):
    global transactions
    transactions = [t for t in transactions if t.id != transaction_id]
    return {"message": "Transaction deleted successfully"}

@app.put("/transactions/{transaction_id}")
def update_transaction(transaction_id: int, updated: Transaction):
    for i, t in enumerate(transactions):
        if t.id == transaction_id:
             t.category = updated.category
             t.amount = updated.amount
             t.type = updated.type
             return {"message": "Transaction updated successfully", "transaction": transactions[i]}
    
    return {"message": "Transaction not found"}
