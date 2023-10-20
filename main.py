import csv

from typing import Union

from fastapi import FastAPI, APIRouter, Depends, File, Request, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")


@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse('index.html', context={"request": request})


@app.get("/test")
async def read_item():
    return JSONResponse(content={"message": "Here's your interdimensional portal."})



@app.post("/sendfile")
async def read_item(file: UploadFile = File(...)):    
    file_content = await file.read()
    with open('uploaded_file.csv', 'w') as fw:
        fw.write(file_content.decode('utf-8'))
    
    with open('uploaded_file.csv', 'r') as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
    
        print([row for row in reader])
    return {"message": 'OK'}


