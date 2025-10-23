from fastapi import FastAPI, Form, Request, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="Gerenciador de Itens")

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Banco de dados em memória (lista de dicionários)
itens = []
contador = 1

@app.get("/")
def listar_itens(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "itens": itens})

@app.get("/novo")
def form_criar_item(request: Request):
    return templates.TemplateResponse("create.html", {"request": request})

@app.post("/criar")
def criar_item(nome: str = Form(...), descricao: str = Form(...)):
    global contador
    item = {"id": contador, "nome": nome, "descricao": descricao}
    itens.append(item)
    contador += 1
    return RedirectResponse("/", status_code=303)

@app.get("/editar/{item_id}")
def editar_item(request: Request, item_id: int):
    for item in itens:
        if item["id"] == item_id:
            return templates.TemplateResponse("edit.html", {"request": request, "item": item})
    raise HTTPException(status_code=404, detail="Item não encontrado")

@app.post("/atualizar/{item_id}")
def atualizar_item(item_id: int, nome: str = Form(...), descricao: str = Form(...)):
    for item in itens:
        if item["id"] == item_id:
            item["nome"] = nome
            item["descricao"] = descricao
            return RedirectResponse("/", status_code=303)
    raise HTTPException(status_code=404, detail="Item não encontrado")

@app.get("/deletar/{item_id}")
def deletar_item(item_id: int):
    for item in itens:
        if item["id"] == item_id:
            itens.remove(item)
            return RedirectResponse("/", status_code=303)
    raise HTTPException(status_code=404, detail="Item não encontrado")