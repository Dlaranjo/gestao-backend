from sqlmodel import Session, select
from models import Projeto, Sprint, Atividade, Planejado, Executado, Usuario

# Projeto CRUD

def get_projetos(session: Session):
    return session.exec(select(Projeto)).all()

def create_projeto(session: Session, projeto: Projeto):
    session.add(projeto)
    session.commit()
    session.refresh(projeto)
    return projeto

def delete_projeto(session: Session, projeto_id: int):
    projeto = session.get(Projeto, projeto_id)
    if projeto:
        session.delete(projeto)
        session.commit()
        return True
    return False

# Sprint CRUD

def get_sprints(session: Session):
    return session.exec(select(Sprint)).all()

def create_sprint(session: Session, sprint: Sprint):
    session.add(sprint)
    session.commit()
    session.refresh(sprint)
    return sprint

def delete_sprint(session: Session, sprint_id: int):
    sprint = session.get(Sprint, sprint_id)
    if sprint:
        session.delete(sprint)
        session.commit()
        return True
    return False

# Atividade CRUD

def get_atividades(session: Session):
    return session.exec(select(Atividade)).all()

def create_atividade(session: Session, atividade: Atividade):
    session.add(atividade)
    session.commit()
    session.refresh(atividade)
    return atividade

def delete_atividade(session: Session, atividade_id: int):
    atividade = session.get(Atividade, atividade_id)
    if atividade:
        session.delete(atividade)
        session.commit()
        return True
    return False

# Planejado CRUD

def get_planejados(session: Session):
    return session.exec(select(Planejado)).all()

def create_planejado(session: Session, planejado: Planejado):
    session.add(planejado)
    session.commit()
    session.refresh(planejado)
    return planejado

def delete_planejado(session: Session, projeto_id: int, sprint_id: int, atividade_id: int):
    planejado = session.get(Planejado, (projeto_id, sprint_id, atividade_id))
    if planejado:
        session.delete(planejado)
        session.commit()
        return True
    return False

# Executado CRUD

def get_executados(session: Session):
    return session.exec(select(Executado)).all()

def create_executado(session: Session, executado: Executado):
    session.add(executado)
    session.commit()
    session.refresh(executado)
    return executado

def delete_executado(session: Session, projeto_id: int, sprint_id: int, atividade_id: int):
    executado = session.get(Executado, (projeto_id, sprint_id, atividade_id))
    if executado:
        session.delete(executado)
        session.commit()
        return True
    return False

# Usuario CRUD

def get_usuarios(session: Session):
    return session.exec(select(Usuario)).all()

def create_usuario(session: Session, usuario: Usuario):
    session.add(usuario)
    session.commit()
    session.refresh(usuario)
    return usuario

def delete_usuario(session: Session, usuario_id: str):
    usuario = session.get(Usuario, usuario_id)
    if usuario:
        session.delete(usuario)
        session.commit()
        return True
    return False 