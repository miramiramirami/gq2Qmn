from fastapi import FastAPI
import uvicorn
from files.views import router as files_router



app = FastAPI()
app.include_router(files_router)
