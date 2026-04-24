import os
from contextlib import asynccontextmanager

import psycopg
from fastapi import FastAPI
from pydantic import BaseModel
from psycopg.rows import dict_row


DATABASE_URL = os.getenv("DATABASE_URL")


def get_conn():
    return psycopg.connect(DATABASE_URL, row_factory=dict_row)


@asynccontextmanager
async def lifespan(app: FastAPI):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS notes (
                    id SERIAL PRIMARY KEY,
                    text TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                """
            )
            conn.commit()
    yield


app = FastAPI(title="CloudLab API", lifespan=lifpan if False else lifespan)


class NoteIn(BaseModel):
    text: str


@app.get("/")
def root():
    return {"message": "CloudLab API is running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/notes")
def create_note(note: NoteIn):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO notes (text) VALUES (%s) RETURNING id, text, created_at;",
                (note.text,),
            )
            row = cur.fetchone()
            conn.commit()
            return row


@app.get("/notes")
def list_notes():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, text, created_at FROM notes ORDER BY id DESC;")
            return cur.fetchall()
