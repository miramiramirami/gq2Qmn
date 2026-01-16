import csv
import os

from fastapi import APIRouter, UploadFile, File, HTTPException
import aiofiles
from datetime import datetime


router = APIRouter(prefix='/api', tags=["FILES"])


UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post('/files/upload')
async def upload_files(file: UploadFile = File(...)):
    file_location = os.path.join(UPLOAD_DIR, file.filename)

    async with aiofiles.open(file_location, "wb") as buffer:
        await buffer.write(await file.read())

    return {"result": f"file {file.filename} uploaded "}


@router.get('/files/get-csv-data')
async def get_csv_data(filename: str):
    safe_name = os.path.basename(filename)
    file_path = f"{UPLOAD_DIR}/{safe_name}"

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    async with aiofiles.open(file_path, "r") as file:
        content = await file.read()
        lines = content.splitlines()
        reader = csv.DictReader(lines)
        result = [row for row in reader]

    return {"lines": result}


@router.post('/files/write-csv')
async def get_csv_data(data: list[dict]):
    if not data:
        return {"mess": "No data provided"}

    now = datetime.now()
    timestamp = now.strftime("%H-%M-%S")
    file_path = os.path.join(UPLOAD_DIR, f"output-{timestamp}.csv")

    fieldnames = data[0].keys()

    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

    return {"mess": "success"}
























