# routes.py
from fastapi import APIRouter, HTTPException
from app.models import Student,UpdateStudent
from bson import ObjectId
from typing import Dict, Optional
from app.database import student_collection



router = APIRouter()


def str_objectid(id: ObjectId) -> str:
    return str(id)

# POST API to create a student
@router.post("/students/", response_model=Dict[str, str], status_code=201)
async def create_student(student: Student):
    student_dict = student.dict()
    try:
        result = await student_collection.insert_one(student_dict)
        return {"id": str_objectid(result.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error while creating student: " + str(e))



#Get API to list all students
@router.get("/students", response_model=dict)
async def filter_students(
    country: Optional[str] = None, 
    age: Optional[int] = None
):
   
    query = {}

    
    if country:
        query["address.country"] = country
    if age is not None:
        query["age"] = {"$gte": age}

    cursor = student_collection.find(query, {"_id": 0, "name": 1, "age": 1})
    students = await cursor.to_list(length=None)
    result = [{"name": student["name"], "age": student["age"]} for student in students]

    return {"data": result}
    
    
#Get students by id
@router.get("/students/{id}", response_model=Student)
async def get_student(id: str):
    try:
        
        student_data = await student_collection.find_one({"_id": ObjectId(id)})
        
        if student_data is None:
            raise HTTPException(status_code=404, detail="Student not found")

        return Student(
            name=student_data["name"],
            age=student_data["age"],
            address=student_data["address"]
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



#Update the students by id 
@router.patch("/students/{id}")
async def update_student(id: str, student: UpdateStudent):
    update_data = student.dict(exclude_unset=True)  
    
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields provided to update")

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
    
    
    
#Delete the students by id 
@router.delete("/students/{id}")
async def delete_student(id: str):
    try:
        result = await student_collection.delete_one({"_id": ObjectId(id)})

        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Student not found")

        return {"status": "success", "detail": "Student deleted successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error while deleting student: {str(e)}")
    
    


