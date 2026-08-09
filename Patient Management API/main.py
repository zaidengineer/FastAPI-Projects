from fastapi import FastAPI,Path,HTTPException,Query
from data_validation import Patient, patient_update
from fastapi.responses import JSONResponse

from database import get_connection
app=FastAPI()


@app.get("/")
def hello():
    return {'message':'Patient Mangement System API'}


@app.get("/about")
def about():
    return {'message': 'A fully functional API to manage your patient records'}


@app.get("/view")
def view():
    connection=get_connection()
    cursor=connection.cursor(dictionary=True,buffered=True)
    cursor.execute("SELECT * FROM patients")
    data=cursor.fetchall()
    cursor.close()
    connection.close()
    patients = []

    for row in data:
        patient = Patient(**row)
        patients.append(patient.model_dump())

    return patients


@app.get('/patient/{patient_id}')
def view_patient(patient_id: str =Path(..., description="ID of the patient in the DB",example="P001")):
     connection=get_connection()
     cursor=connection.cursor(dictionary=True,buffered=True)
     query="""
        SELECT * FROM patients
        WHERE id=%s     
    """
     values=(patient_id,)
     cursor.execute(query,values)
     data=cursor.fetchone()
     cursor.close()
     connection.close()
     if not data:
        raise HTTPException(status_code=404, detail='Patient not found')
     patient = Patient(**data)

     return patient.model_dump()


@app.post("/create")
def add_patient(patient:Patient):
    connection=get_connection()
    cursor=connection.cursor(dictionary=True,buffered=True)
    #check if id already exists
    query="""
    SELECT id 
    FROM patients
    WHERE id=%s
    """
    cursor.execute(query,(patient.id,))
    existingpatient=cursor.fetchone()
    if existingpatient is not None:
        cursor.close()
        connection.close()
        raise HTTPException(status_code=400, detail="Patient with this id already exists")
    # insert patient data
    query="""
    INSERT INTO patients (id, name, age, city, gender, height, weight)
    VALUES
    (%s, %s, %s, %s, %s, %s, %s)"""
    values=(
        patient.id,
        patient.name,
        patient.age,
        patient.city,
        patient.gender,
        patient.height,
        patient.weight
    )
    cursor.execute(query,values)
    connection.commit()
    cursor.close()
    connection.close()
    return JSONResponse(status_code=201, content={'message':'patient data created successfully'})


@app.get('/sort')
def sort_patient(sort_by: str =Query(..., description='Sort on the basis of height, weight, '
'or bmi'), order: str =Query('asc',description='sort in the asc or dsc order') ):
    valid_fields=['height','weight','bmi']
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400,detail='Invalid field')
    if order not in ['asc', 'dsc']:
        raise HTTPException(status_code=400, detail='Invalid order select between asc or dsc')

    connection=get_connection()
    cursor=connection.cursor(dictionary=True,buffered=True)
    if sort_by=="bmi":
        query="SELECT * FROM patients"
        cursor.execute(query)
        pat_data=cursor.fetchall()

        patients=[]
        for row in pat_data:
            patient=Patient(**row)
            patients.append(patient)


        sorted_order= True if order=='dsc' else False

        sorted_data=sorted(patients,
            key=lambda patient:patient.bmi,
            reverse=sorted_order
        )
        cursor.close()
        connection.close()
        return [
        patient.model_dump()
        for patient in sorted_data
        ]


    allowed_sort_fields = {
        "height": "height",
        "weight": "weight"
    }

    sort_column = allowed_sort_fields[sort_by]

    sort_order = "DESC" if order == "dsc" else "ASC"

    query = f"""
    SELECT *
    FROM patients
    ORDER BY {sort_column} {sort_order}
    """

    cursor.execute(query)

    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    patients = []

    for row in rows:
        patient = Patient(**row)
        patients.append(patient.model_dump())

    return patients


@app.put("/update/{patient_id}")
def update_patient(patient_id:str, patient_info:patient_update):
    connection=get_connection()
    cursor=connection.cursor(dictionary=True,buffered=True)
    query="""
    SELECT id FROM patients
    WHERE id=%s"""
    values=(patient_id,)
    cursor.execute(query,values)
    data=cursor.fetchone()
    if data is None:
        cursor.close()
        connection.close()
        raise HTTPException(status_code=404, detail="patient not found")
    #update data
    updated_data=patient_info.model_dump(exclude_unset=True)
    if not updated_data:
        cursor.close()
        connection.close()
        raise HTTPException(status_code=400, detail="No fields provided for update")

    allowed_fields={
       "name",
       "age",
       "city",
       "gender",
       "height",
       "weight"
       }
    updated_parts=[]
    values=[]
    for field, value in updated_data.items():
        if field not  in allowed_fields:
            continue
        updated_parts.append(f"{field} = %s")
        values.append(value)
    values.append(patient_id)
    query=f"""
    UPDATE patients
    SET {",".join(updated_parts)}
    WHERE id=%s"""
    cursor.execute(query,tuple(values))
    connection.commit()
    cursor.close()
    connection.close()
    return JSONResponse(status_code=200,content={"message":"patient updated successfully"})