import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client
from pydantic import BaseModel
from datetime import date
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Разрешаем запросы с фронтенда (вашего сайта)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение к Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Модель данных для записи
class EntryCreate(BaseModel):
    user_id: str
    date: date
    time: Optional[str] = None
    anxiety: Optional[int] = None
    apathy: Optional[int] = None
    headache: Optional[int] = None
    sleep_hours: Optional[float] = None
    sleep_quality: Optional[int] = None
    sleep_character: Optional[str] = None
    sleep_comment: Optional[str] = None
    medication: Optional[str] = None
    trigger: Optional[str] = None
    delayed_trigger: Optional[str] = None
    note: Optional[str] = None

# Эндпоинт: добавить запись
@app.post("/add_entry")
def add_entry(entry: EntryCreate):
    try:
        response = supabase.table("entries").insert(entry.dict()).execute()
        return {"status": "ok", "data": response.data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Эндпоинт: получить все записи пользователя
@app.get("/get_entries/{user_id}")
def get_entries(user_id: str):
    try:
        response = supabase.table("entries").select("*").eq("user_id", user_id).order("date").execute()
        return {"status": "ok", "data": response.data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Проверка, что сервер жив
@app.get("/")
def root():
    return {"message": "Твой трекер работает! 🚀"}