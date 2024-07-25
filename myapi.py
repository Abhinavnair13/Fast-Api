from typing import Optional

import uvicorn
from fastapi import FastAPI,Path,Query
from pydantic import BaseModel

app = FastAPI()
@app.get("/")
def index():
    return {"name": "First_name"}
students = {
    1: {
        "name" : "Jhon",
        "age" : 20,
        "Majors" : "CSE"
    }  ,
    2: {
        "name" : "Lenny",
        "age" : 20,
        "Majors" : "CSE"
    } ,
    3: {
        "name" : "ben",
        "age" : 20,
        "Majors" : "CSE"
    }

}
class Student(BaseModel):
    name : str
    age : int
    Majors : str
class UpdateStudent(BaseModel):
    name : Optional[str] = None
    age : Optional[int] = None
    Majors : Optional[str] = None
@app.get("/get-student/{student_id}")
def get_student(student_id: int = Path(...,description = "The id of the student you want to view", gt=0,lt=10)):
    return students[student_id]

@app.get("/get_by_name")
def get_student_by_name(*,name: Optional[str]= None,test: int):
    for student_id in students:
        if students[student_id]["name"].lower()==name.lower():
            return students[student_id]
    return {"Data" : "not found"}

@app.get("/get_by_name_or_id/")
def get_student_by_name_id(
        student_id : Optional[int] = Query(None,description="This is the id field",gt = 0,lt=4),
        name: Optional[str]  = Query(None,description = "This is the name field")):
    #By default, FastAPI expects query parameters to be explicitly declared using the Query function.
    if not student_id and not name:
        return {"Data" : "No values inputted"}
    student_obj = students.get(student_id)
    if student_obj:
        return student_obj
    for student_id in students:
        if students[student_id]["name"].lower()==name.lower():
            return students[student_id]
    return {"Data" : "Not found"}

@app.post("/create-student/{student_id}")
def create_student(student_id : int, student : Student):
    if student_id in students:
        return {"Error" : "Student already exists"}
    students[student_id] = student
    return students[student_id]

@app.put("/update-student/{student_id}")
def update_student(student_id: int,student: UpdateStudent):
    if student_id not in students:
        return  {"Error": "Student id invalid"}
    if student.name != None:
        students[student_id]["name"] = student.name
    if student.Majors != None:
        students[student_id]["Majors"] = student.Majors
    if student.age != None:
        students[student_id]["age"] = student.age
    return students[student_id]

@app.delete("/delete-student/{student_id}")
def delete_student(student_id : int):
    if student_id not in students:
        return {"Error" : "Students not exits"}
    del students[student_id]
    return {"Message" : "Student deleted successfully"}

if __name__ == '__main__':
    uvicorn.run("myapi:app", host='127.0.0.1', port=8001 ,reload=True)