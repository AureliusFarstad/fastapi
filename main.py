from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import jieba 
import jieba.posseg as pseg

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:5173",
    "http://127.0.0.1:5173/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Text(BaseModel):
    lang: str | None = None
    text: str

@app.post("/segment/")
async def segment_chinese(text: Text):
    segments = jieba.cut(text.text)
    return {"segments": segments}

@app.post("/segment_pos/")
async def segment_chinese(text: Text):
    segments = pseg.cut(text.text)
    return {"segments": segments}