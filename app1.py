from fastapi import FastAPI

app = FastAPI()

customers = {
     101: {"name": "John Doe", "email": "john.doe@example.com"},
     102: {"name": "Jane Smith", "email": "jane.smith@example.com"},
     103: {"name": "Bob Johnson", "email": "bob.johnson@example.com"},
     104: {"name": "Alice Brown", "email": "alice.brown@example.com"}
}

@app.get("/customers/{customer_id}")
def get_customer(customer_id: int):
    if customer_id not in customers:
        return {"error": "Customer not found"}
    else:
        return customers[customer_id]