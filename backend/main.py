from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from bson import ObjectId

from pymongo import MongoClient
from pydantic import BaseModel

from typing import List
import uvicorn
import os

import argparse


MONGO_PORT = os.getenv('MONGO_PORT', '27017')
MONGO_HOST = os.getenv('MONGO_HOST', 'localhost')
MONGO_PASSWORD = os.getenv('MONGO_INITDB_ROOT_PASSWORD', 'root')
MONGO_USER = os.getenv('MONGO_INITDB_ROOT_USERNAME', 'root')
MONGODB_ADDRESS = f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/"
ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:4200').split(',')
FASTAPI_ROOT_PATH = os.getenv('FASTAPI_ROOT_PATH', '')

print('FAST API ROOT PATH: ', FASTAPI_ROOT_PATH)

app = FastAPI(root_path=FASTAPI_ROOT_PATH)
app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

client = MongoClient(MONGODB_ADDRESS)
db = client['test_db']
collection = db['students']

class Student(BaseModel):
    name: str
    age: int

@app.get("/health")
async def ping():
    return {'status': 'success'}

@app.post("/student")
async def create_student(new_student: Student):
    print('Create student request')   
    result = collection.insert_one(new_student.dict())
    return {"student": {**new_student.dict(), 'id': str(result.inserted_id)}}

@app.get("/student/{id}")
async def read_student(id: str):
    student = collection.find_one({'_id': ObjectId(id)})
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    student['id'] = str(student.pop('_id'))
    return student

@app.get("/students")
async def get_all_students():
    print('Get all students request')  
    students = []
    students = list(collection.find())

    for student in students:
        student['id'] = str(student.pop('_id'))

    return{"students": students}

@app.put("/student/{id}")
async def update_student(id: str, updated_student: Student):
    result = collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": updated_student.dict()})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student updated"}

@app.delete("/student/{id}")
async def delete_student(id: str):
    result = collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student deleted"}


def argparser():
    parser = argparse.ArgumentParser()

    parser.add_argument('-e', '--env', default='dev')

    return parser.parse_args()

if __name__ == '__main__':
    args = argparser()
    env = args.env    

    uvicorn.run('main:app', host="0.0.0.0", port=8000, reload=True)
