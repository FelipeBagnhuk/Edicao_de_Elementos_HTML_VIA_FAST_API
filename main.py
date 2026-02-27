from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional
import json
from pathlib import Path
from datetime import datetime

app = FastAPI(title="Título Control", description="Controla o título do seu HTML via API")

DB_FILE = Path("title_db.json")

class TitleInput(BaseModel):
    titulo: str

class Output(BaseModel):
    titulo: str
    timestamp: str

def load_title() -> str:
    if DB_FILE.exists():
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('title', 'default title')
    return 'default title'

def save_title(title: str):
    data = {
        'title': title,
        'timestamp': datetime.now().isoformat()
    }
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.get("/", tags=["HTML"])
async def get_html():
    """Serve o HTML com o título atual do 'banco'"""
    titulo_atual = load_title()
    
    html = f"""
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{titulo_atual}</title>
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{ font-family: system-ui, sans-serif; line-height: 1.6; padding: 20px; background: #f0f2f5; }}
            .container {{ max-width: 800px; margin: 0 auto; background: white; border-radius: 12px; box-shadow: 0 8px 32px rgba(0,0,0,0.1); overflow: hidden; }}
            .imagem {{ width: 100%; height: 250px; object-fit: cover; }}
            .conteudo {{ padding: 30px; }}
            .titulo {{ font-size: 2.2em; font-weight: 700; color: #1a202c; margin-bottom: 20px; }}
            .texto {{ font-size: 1.1em; color: #4a5568; }}
            @media (max-width: 600px) {{ .titulo {{ font-size: 1.6em; }} .conteudo {{ padding: 20px; }} }}
        </style>
    </head>
    <body>
        <div class="container">
            <img src="sua-imagem.jpg" alt="Imagem do projeto" class="imagem">
            <div class="conteudo">
                <h1 class="titulo">{titulo_atual}</h1>
                <p class="texto">
                    Seu conteúdo aqui... O título é controlado via API e sempre atualizado!
                </p>
            </div>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html)

@app.post("/titulo/", response_model=Output, tags=["API"])
async def atualizar_titulo(request: TitleInput):
    """Atualiza o título (salva no arquivo e sobrescreve o anterior)"""
    save_title(request.titulo)
    return Output(
        titulo=request.titulo,
        timestamp="Atualizado agora"
    )

@app.get("/titulo/", response_model=Output, tags=["API"])
async def get_titulo():
    """Pega o título atual salvo"""
    titulo = load_title()
    return Output(titulo=titulo, timestamp="Atual")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
