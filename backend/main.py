from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from bson import ObjectId

from pymongo import MongoClient
from pydantic import BaseModel

from typing import List
import uvicorn
import os

import argparse


MONGODB_PORT = os.getenv('MONGODB_PORT', '27017')
MONGODB_HOST = os.getenv('MONGODB_HOST', 'localhost')
PASSWORD = os.getenv('PASSWORD', 'root')
USERNAME = os.getenv('USERNAME', 'root')
MONGODB_ADDRESS = f"mongodb://{USERNAME}:{PASSWORD}@{MONGODB_HOST}:{MONGODB_PORT}/"
ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:4200').split(',')

app = FastAPI()
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

@app.get("/")
async def ping():
    return 'The server is up'

@app.post("/student")
async def create_student(new_student: Student):
    print('Create student request')   
    result = collection.insert_one(new_student.dict())
    return {"student": {**new_student.dict(), 'id': str(result.inserted_id)}}

'''
@app.post("/students")
async def create_students(new_students: List[Student]):
    result = collection.insert_one()
    # Insert students into the collection
    result = collection.insert_many([student.dict() for student in new_students])
    return {"inserted_ids": [str(_id) for _id in result.inserted_ids]}
'''

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
    parser.add_argument('-p', '--password', default='root')
    parser.add_argument('-u', '--username', default='root')

    return parser.parse_args()

if __name__ == '__main__':
    args = argparser()
    env = args.env    

    uvicorn.run('main:app', host="0.0.0.0", port=21950, reload=True)
