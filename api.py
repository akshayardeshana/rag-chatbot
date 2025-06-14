from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from db import insert_complaint, get_complaint_by_complaint_id, init_db

app = FastAPI()
init_db()

class Complaint(BaseModel):
    name: str
    email: str
    phone_number: str
    complaint_details: str

@app.post("/complaints")
def create_complaint(data: Complaint):
    complaint_id = insert_complaint(data.name, data.email, data.phone_number, data.complaint_details)
    return {"complaint_id": complaint_id, "message": "Complaint registered successfully"}

@app.get("/complaints/{complaint_id}")
def fetch_complaint(complaint_id: str):
    record = get_complaint_by_complaint_id(complaint_id)
    if not record:
        raise HTTPException(status_code=404, detail="Complaint not found")
    keys = ["complaint_id", "name", "phone_number", "complaint_details", "status", "created_at"]
    return dict(zip(keys, record))