from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session
from database import get_session, init_db
from models import Projeto, Sprint, Atividade, Executado, Usuario, ProjetoRead
from fastapi.middleware.cors import CORSMiddleware
import crud
from typing import List
from sqlmodel import select

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
@app.get("/projetos", response_model=List[ProjetoRead])
def read_projetos(session: Session = Depends(get_session)):
    projetos = crud.get_projetos_nested(session)
    return [ProjetoRead.from_orm(projeto) for projeto in projetos]

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

@app.get("/projetos/{projeto_id}/atividades")
def get_atividades_for_project(projeto_id: int, session: Session = Depends(get_session)):
    atividades = session.exec(select(Atividade).where(Atividade.ProjetoID == projeto_id)).all()
    sprints = session.exec(select(Sprint).where(Sprint.ProjetoID == projeto_id)).all()
    sprint_map = {s.SprintID: s.SprintNome for s in sprints}
    atividades_with_sprint_nome = []
    for atividade in atividades:
        atividade_dict = atividade.dict()
        atividade_dict["SprintNome"] = sprint_map.get(atividade.SprintID, "")
        atividades_with_sprint_nome.append(atividade_dict)
    return atividades_with_sprint_nome

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

# Executado endpoints
@app.get("/executados")
def read_executados(session: Session = Depends(get_session)):
    return crud.get_executados(session)

@app.post("/executados")
def create_executado(executado: Executado, session: Session = Depends(get_session)):
    return crud.create_executado(session, executado)

@app.put("/executados/{executado_id}")
def update_executado(executado_id: int, executado: Executado, session: Session = Depends(get_session)):
    db_obj = session.get(Executado, executado_id)
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