from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session
from database import get_session, init_db
from models import Projeto, Sprint, Atividade, Planejado, Executado, Usuario
from fastapi.middleware.cors import CORSMiddleware
import crud

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=False,  # Disable credentials
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

@app.on_event("startup")
def on_startup():
    init_db()

# Projeto endpoints
@app.get("/projetos")
def read_projetos(session: Session = Depends(get_session)):
    return crud.get_projetos(session)

@app.post("/projetos")
def create_projeto(projeto: Projeto, session: Session = Depends(get_session)):
    return crud.create_projeto(session, projeto)

@app.put("/projetos/{projeto_id}")
def update_projeto(projeto_id: int, projeto: Projeto, session: Session = Depends(get_session)):
    db_obj = session.get(Projeto, projeto_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Projeto not found")
    for key, value in projeto.dict(exclude_unset=True).items():
        setattr(db_obj, key, value)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj

@app.delete("/projetos/{projeto_id}")
def delete_projeto(projeto_id: int, session: Session = Depends(get_session)):
    if not crud.delete_projeto(session, projeto_id):
        raise HTTPException(status_code=404, detail="Projeto not found")
    return {"message": "Projeto deleted successfully"}

# Sprint endpoints
@app.get("/sprints")
def read_sprints(session: Session = Depends(get_session)):
    return crud.get_sprints(session)

@app.post("/sprints")
def create_sprint(sprint: Sprint, session: Session = Depends(get_session)):
    return crud.create_sprint(session, sprint)

@app.put("/sprints/{sprint_id}")
def update_sprint(sprint_id: int, sprint: Sprint, session: Session = Depends(get_session)):
    db_obj = session.get(Sprint, sprint_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Sprint not found")
    for key, value in sprint.dict(exclude_unset=True).items():
        setattr(db_obj, key, value)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj

@app.delete("/sprints/{sprint_id}")
def delete_sprint(sprint_id: int, session: Session = Depends(get_session)):
    if not crud.delete_sprint(session, sprint_id):
        raise HTTPException(status_code=404, detail="Sprint not found")
    return {"message": "Sprint deleted successfully"}

# Atividade endpoints
@app.get("/atividades")
def read_atividades(session: Session = Depends(get_session)):
    return crud.get_atividades(session)

@app.post("/atividades")
def create_atividade(atividade: Atividade, session: Session = Depends(get_session)):
    return crud.create_atividade(session, atividade)

@app.put("/atividades/{atividade_id}")
def update_atividade(atividade_id: int, atividade: Atividade, session: Session = Depends(get_session)):
    db_obj = session.get(Atividade, atividade_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Atividade not found")
    for key, value in atividade.dict(exclude_unset=True).items():
        setattr(db_obj, key, value)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj

@app.delete("/atividades/{atividade_id}")
def delete_atividade(atividade_id: int, session: Session = Depends(get_session)):
    if not crud.delete_atividade(session, atividade_id):
        raise HTTPException(status_code=404, detail="Atividade not found")
    return {"message": "Atividade deleted successfully"}

# Planejado endpoints
@app.get("/planejados")
def read_planejados(session: Session = Depends(get_session)):
    return crud.get_planejados(session)

@app.post("/planejados")
def create_planejado(planejado: Planejado, session: Session = Depends(get_session)):
    return crud.create_planejado(session, planejado)

@app.put("/planejados/{projeto_id}/{sprint_id}/{atividade_id}")
def update_planejado(projeto_id: int, sprint_id: int, atividade_id: int, planejado: Planejado, session: Session = Depends(get_session)):
    db_obj = session.get(Planejado, (projeto_id, sprint_id, atividade_id))
    if not db_obj:
        raise HTTPException(status_code=404, detail="Planejado not found")
    for key, value in planejado.dict(exclude_unset=True).items():
        setattr(db_obj, key, value)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj

@app.delete("/planejados/{projeto_id}/{sprint_id}/{atividade_id}")
def delete_planejado(projeto_id: int, sprint_id: int, atividade_id: int, session: Session = Depends(get_session)):
    if not crud.delete_planejado(session, projeto_id, sprint_id, atividade_id):
        raise HTTPException(status_code=404, detail="Planejado not found")
    return {"message": "Planejado deleted successfully"}

# Executado endpoints
@app.get("/executados")
def read_executados(session: Session = Depends(get_session)):
    return crud.get_executados(session)

@app.post("/executados")
def create_executado(executado: Executado, session: Session = Depends(get_session)):
    return crud.create_executado(session, executado)

@app.put("/executados/{projeto_id}/{sprint_id}/{atividade_id}")
def update_executado(projeto_id: int, sprint_id: int, atividade_id: int, executado: Executado, session: Session = Depends(get_session)):
    db_obj = session.get(Executado, (projeto_id, sprint_id, atividade_id))
    if not db_obj:
        raise HTTPException(status_code=404, detail="Executado not found")
    for key, value in executado.dict(exclude_unset=True).items():
        setattr(db_obj, key, value)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj

@app.delete("/executados/{projeto_id}/{sprint_id}/{atividade_id}")
def delete_executado(projeto_id: int, sprint_id: int, atividade_id: int, session: Session = Depends(get_session)):
    if not crud.delete_executado(session, projeto_id, sprint_id, atividade_id):
        raise HTTPException(status_code=404, detail="Executado not found")
    return {"message": "Executado deleted successfully"}

# Usuario endpoints
@app.get("/usuarios")
def read_usuarios(session: Session = Depends(get_session)):
    return crud.get_usuarios(session)

@app.post("/usuarios")
def create_usuario(usuario: Usuario, session: Session = Depends(get_session)):
    return crud.create_usuario(session, usuario)

@app.put("/usuarios/{usuario_id}")
def update_usuario(usuario_id: str, usuario: Usuario, session: Session = Depends(get_session)):
    db_obj = session.get(Usuario, usuario_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Usuario not found")
    for key, value in usuario.dict(exclude_unset=True).items():
        setattr(db_obj, key, value)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj

@app.delete("/usuarios/{usuario_id}")
def delete_usuario(usuario_id: str, session: Session = Depends(get_session)):
    if not crud.delete_usuario(session, usuario_id):
        raise HTTPException(status_code=404, detail="Usuario not found")
    return {"message": "Usuario deleted successfully"} 