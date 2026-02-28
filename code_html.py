def generate_html(current_title: str) -> str:
    return f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{current_title}</title>
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
        <img src="/static/imagens/imagem1.png" alt="Project Image" class="imagem">
        <div class="conteudo">
            <h1 class="titulo">{current_title}</h1>
            <p class="texto">
                Your content here... Title controlled via API and always updated!
            </p>
        </div>
    </div>
</body>
</html>
"""
