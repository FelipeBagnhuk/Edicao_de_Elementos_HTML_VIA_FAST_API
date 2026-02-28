from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional
import json
from pathlib import Path
from datetime import datetime
from code_html import generate_html
from fastapi.staticfiles import StaticFiles


app = FastAPI(title="Title Control", description="Controls the HTML title via API")
app.mount("/static", StaticFiles(directory="static"), name="static")

DB_FILE = Path("title_db.json")


class TitleInput(BaseModel):
    title: str


class TitleOutput(BaseModel):
    title: str
    timestamp: str


def load_title() -> str:
    if DB_FILE.exists():
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('title', 'Default Title')
    return 'Default Title'


def save_title(title: str):
    data = {
        'title': title,
        'timestamp': datetime.now().isoformat()
    }
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


@app.get("/", tags=["HTML"])
async def get_html():
    """Serves the HTML with the current title from the database"""
    current_title = load_title()
    html = generate_html(current_title)  
    return HTMLResponse(content=html)


@app.post("/title/", response_model=TitleOutput, tags=["API"])
async def update_title(request: TitleInput):
    """Updates the title (saves to file and overwrites previous)"""
    save_title(request.title)
    return TitleOutput(
        title=request.title,
        timestamp="Updated now"
    )


@app.get("/title/", response_model=TitleOutput, tags=["API"])
async def get_title():
    """Gets the current saved title"""
    title = load_title()
    return TitleOutput(title=title, timestamp="Current")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


#rodar uvicorn: uvicorn main:app --reload
#swagger (depois de ter rodado o uvicorn): http://127.0.0.1:8000/docs#

