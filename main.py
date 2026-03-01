from fastapi import FastAPI, HTTPException, File, UploadFile, Form
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional
import json
from pathlib import Path
from datetime import datetime
from code_html import generate_html
from fastapi.staticfiles import StaticFiles
import shutil
import os
from PIL import Image
import mimetypes

app = FastAPI(title="Title Control", description="Controls the HTML title via API")
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

DB_FILE = Path("title_db.json")
CONTENT_FILE = Path("content_db.json")  

class TitleInput(BaseModel):
    title: str

class ContentInput(BaseModel): 
    content: str

class TitleOutput(BaseModel):
    title: str
    timestamp: str

class ContentOutput(BaseModel):  
    content: str
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


def load_content() -> str:
    if CONTENT_FILE.exists():
        with open(CONTENT_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('content', 'Your content here... Title controlled via API and always updated!')
    return 'Your content here... Title controlled via API and always updated!'

def save_content(content: str):
    data = {
        'content': content,
        'timestamp': datetime.now().isoformat()
    }
    with open(CONTENT_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


@app.get("/", tags=["HTML"])
async def get_html():
    """Serves the HTML with the current title AND content from the database"""
    current_title = load_title()
    current_content = load_content()  
    html = generate_html(current_title, current_content)   
    return HTMLResponse(content=html)


@app.post("/title/", response_model=TitleOutput, tags=["API"])
async def update_title(request: TitleInput):
    save_title(request.title)
    return TitleOutput(
        title=request.title,
        timestamp="Updated now"
    )

@app.get("/title/", response_model=TitleOutput, tags=["API"])
async def get_title():
    title = load_title()
    return TitleOutput(title=title, timestamp="Current")


@app.post("/content/", response_model=ContentOutput, tags=["API"])
async def update_content(request: ContentInput):
    """Atualiza o texto do conteúdo do HTML"""
    save_content(request.content)
    return ContentOutput(
        content=request.content,
        timestamp="Updated now"
    )

@app.get("/content/", response_model=ContentOutput, tags=["API"])
async def get_content():
    """Pega o conteúdo atual salvo"""
    content = load_content()
    return ContentOutput(content=content, timestamp="Current")

# Rotas de upload existentes permanecem iguais
@app.post("/upload-image/", tags=["Upload"])
async def upload_image(file: UploadFile = File(..., description="Imagem em qualquer formato")):
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="Arquivo deve ser uma imagem!")
    
    uploads_dir = Path("uploads")
    uploads_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_extension = Path(file.filename).suffix.lower()
    new_filename = f"imagem_{timestamp}{file_extension}"
    file_path = uploads_dir / new_filename
    
    with file.file as buffer:
        shutil.copyfileobj(buffer, open(file_path, 'wb'))
    
    return {
        "message": "Imagem carregada com sucesso!",
        "filename": new_filename,
        "url": f"/uploads/{new_filename}"
    }

@app.get("/images/", tags=["Upload"])
async def list_images():
    uploads_dir = Path("uploads")
    if not uploads_dir.exists():
        return {"images": []}
    
    images = []
    for img_file in uploads_dir.glob("*.png"):
        images.append({"filename": img_file.name, "url": f"/uploads/{img_file.name}"})
    for img_file in uploads_dir.glob("*.jpg"):
        images.append({"filename": img_file.name, "url": f"/uploads/{img_file.name}"})
    for img_file in uploads_dir.glob("*.jpeg"):
        images.append({"filename": img_file.name, "url": f"/uploads/{img_file.name}"})
    
    return {"images": images}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
