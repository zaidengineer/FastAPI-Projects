from fastapi import FastAPI,HTTPException,Path,Query
from fastapi.responses import JSONResponse
from Database.notesdata import load_data,save_data
from datetime import date
from pydant_models.data_validation import Notes, Notes_update, Pinned
app=FastAPI()

@app.get('/')
def home():
    dic={'message':'Notes Management API'}
    return dic

@app.get('/notes')
def allnotes(skip:int=Query(0,ge=0),limit:int=Query(10,ge=1,le=100)):
    data=load_data()
    notes=list(data.items())
    return dict(notes[skip:skip + limit])

@app.get('/notesid/{notes_id}')
def searchnotes(notes_id:str=Path(..., examples=["N001"])):
    data=load_data()
    if notes_id not in data:
        raise HTTPException(status_code=404, detail="Id not found")
    return data[notes_id]

@app.get('/sort')
def sortnotes(sort_by:str=Query(..., description="sort on the basis of title,category"),order:str=Query(..., description="sort in asc or dsc")):
    data=load_data()
    valid_fields=["title","category"]
    valid_order=['asc','dsc']
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400,detail="Invalid Field")
    if order not in valid_order:
        raise HTTPException (status_code=400, detail="Invalid Order")
    sorted_order=True if order=='dsc' else False
    sorted_data=sorted(data.values(),key=lambda x:x.get(sort_by,0), reverse=sorted_order)
    return sorted_data

@app.get('/notes/filter')
def filternotes(category:str=Query(..., description="Category")):
    data=load_data()
    filtered={}
    for note_id, note in data.items():
        if note["category"].lower()==category.lower():
            filtered[note_id]=note
    return filtered

@app.post('/create')
def createnotes(note:Notes):
    data=load_data()
    if note.id in data:
        raise HTTPException(status_code=409, detail="This id already exist")
    newdata={
        'id':note.id,
        'title':note.title,
        'category':note.category,
        'tags':note.tags,
        'content':note.content,
        'created_date':date.today().isoformat(),
        'is_pinned':False
    }
    data[note.id]=newdata
    save_data(data)
    return JSONResponse(status_code=201, content={'message':'New note created successfully'})

@app.put('/update/{notes_id}')
def updatenote(notes_update:Notes_update,notes_id:str=Path(..., examples=["N001"])):
    data=load_data()
    if notes_id not in data:
        raise HTTPException(status_code=404, detail="id not found")
    existing_info=data[notes_id]
    newinfo=notes_update.model_dump(exclude_unset=True)
    for key,value in newinfo.items():
        existing_info[key]=value
    data[notes_id]=existing_info
    save_data(data)
    return JSONResponse(status_code=200, content={'message':'Notes updated successfully'})

@app.delete('/remove/{notes_id}')
def removenotes(notes_id:str=Path(..., examples=["N001"])):
    data=load_data()
    if notes_id not in data:
        raise HTTPException(status_code=404, detail="id not found")
    del data[notes_id]
    save_data(data)
    return JSONResponse(status_code=200, content={'message':'Note deleted successfully'})

@app.patch('/notes/{notes_id}/pin')
def pin(pin:Pinned,notes_id:str=Path(..., examples=["N001"])):
    data=load_data()
    if notes_id not in data:
        raise HTTPException (status_code= 404, detail="id not found")
    data[notes_id]['is_pinned']=pin.is_pinned
    save_data(data)
    return JSONResponse(status_code=200, content={'message':'Updated successfully'})