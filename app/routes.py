# routes.py
from fastapi import APIRouter, HTTPException, Query
from app.models import Student, StudentFilter, StudentListResponse, UpdateStudent
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from typing import Dict, Optional
from app.database import student_collection





# Create a router for the student-related routes
router = APIRouter()

# Helper function to convert MongoDB object ID to string
def str_objectid(id: ObjectId) -> str:
    return str(id)

# POST API to create a student
@router.post("/students/", response_model=Dict[str, str], status_code=201)
async def create_student(student: Student):
    student_dict = student.dict()
    # Insert student into MongoDB collection
    try:
        result = await student_collection.insert_one(student_dict)
        # Return the inserted student ID
        return {"id": str_objectid(result.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error while creating student: " + str(e))
    
    
    
    

@router.get("/students/{id}", response_model=Student)
async def get_student(id: str):
    try:
        # Convert the string id to ObjectId for MongoDB query
        student_data = await student_collection.find_one({"_id": ObjectId(id)})
        
        if student_data is None:
            raise HTTPException(status_code=404, detail="Student not found")

        # Convert MongoDB document to Pydantic model
        return Student(
            name=student_data["name"],
            age=student_data["age"],
            address=student_data["address"]
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




@router.patch("/students/{id}")
async def update_student(id: str, student: UpdateStudent):
    # Prepare the data for update
    update_data = student.dict(exclude_unset=True)  # Only include fields that are provided
    
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields provided to update")

    # Convert the student ID from string to ObjectId for MongoDB query
    try:
        result = await student_collection.update_one(
            {"_id": ObjectId(id)}, 
            {"$set": update_data}
        )

        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Student not found")

        return {"status": "success", "detail": "Student updated successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error while updating student: {str(e)}")
    
    
    
    
@router.delete("/students/{id}")
async def delete_student(id: str):
    try:
        # Attempt to delete the student by ID
        result = await student_collection.delete_one({"_id": ObjectId(id)})

        # If no documents are matched, raise a 404 error
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Student not found")

        return {"status": "success", "detail": "Student deleted successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error while deleting student: {str(e)}")
    
    
@router.get("/students")
async def list_students(
    country: Optional[str] = Query(None, description="Filter students by country"),
    age: Optional[int] = Query(None, description="Filter students by age (greater than or equal to)")
):
    try:
        # Build the query filter based on provided query parameters
        filter_query = {}

        if country:
            filter_query["address.country"] = country

        if age is not None:
            filter_query["age"] = {"$gte": age}  # Only include students with age >= provided value

        # Fetch students based on the filter query
        students = await student_collection.find(filter_query).to_list(length=100)

        # Return the list of students
        return {"status": "success", "students": students}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error while fetching students: {str(e)}")   
    
    
def convert_objectid_to_str(data):
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, ObjectId):
                data[key] = str(value)  # Convert ObjectId to string
            elif isinstance(value, list):
                data[key] = [convert_objectid_to_str(item) for item in value]
    return data

@router.get("/students", response_model=dict)
async def get_students(country: str = None, age: int = None):
    # Building the query based on filters
    query = {}
    if country:
        query["address.country"] = country
    if age:
        query["age"] = age

    # Fetch the data from MongoDB based on the filters
    students = student_collection.find(query)

    # Prepare the response
    response_data = []
    for student in students:
        # Convert the ObjectId and map the desired fields (name, age)
        student_data = {
            "name": student["name"],
            "age": student["age"]
        }
        
        # Convert ObjectId fields to string, if any
        student_data = convert_objectid_to_str(student_data)
        response_data.append(student_data)

    # Return the filtered data as JSON response
    return {"data": response_data}