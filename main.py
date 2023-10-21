import csv
import os

from typing import Union

from fastapi import FastAPI, APIRouter, Depends, File, Request, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from compute_quantity_limits import save_image, save_correct_csv


OLD_DATA_GRAPH_PATH = 'static/resources/old_data_graph.png'
ORIGINAL_DATA_FILE_PATH = 'static/resources/uploaded_file.csv'
NEW_DATA_GRAPH_PATH = 'static/resources/new_data_graph.png'
CORRECTED_DATA_FILE_PATH = 'static/resources/corrected_data.csv'


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")


@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse('index.html', context={"request": request})


@app.post("/sendfile")
async def read_item(request: Request, file: UploadFile):   
    file_content = await file.read()
    with open(ORIGINAL_DATA_FILE_PATH, 'w') as fw:
        fw.write(file_content.decode('utf-8'))
    
    with open(ORIGINAL_DATA_FILE_PATH, 'r') as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
    
    save_image(data_path=ORIGINAL_DATA_FILE_PATH, output_image_name=OLD_DATA_GRAPH_PATH)
    save_correct_csv(input_dataset=ORIGINAL_DATA_FILE_PATH, output_dataset=CORRECTED_DATA_FILE_PATH, output_image=NEW_DATA_GRAPH_PATH)
    return templates.TemplateResponse('index.html', context={"request": request, 'd': OLD_DATA_GRAPH_PATH})


@app.get('/about')
async def about(request: Request):
    return templates.TemplateResponse('about.html', context={"request": request, 'path': 'static/resources/graph.img'})



