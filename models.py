from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date

class Projeto(SQLModel, table=True):
    ProjetoID: Optional[int] = Field(default=None, primary_key=True)
    Nome: str
    DataInicio: str
    DataFim: str
    GerenteProjeto: str
    SolicitanteProjeto: str

class Sprint(SQLModel, table=True):
    SprintID: Optional[int] = Field(default=None, primary_key=True)
    ProjetoID: int
    SprintNome: str
    SprintDataInicio: str
    SprintDataFim: str

class Atividade(SQLModel, table=True):
    AtividadeID: Optional[int] = Field(default=None, primary_key=True)
    ProjetoID: int
    SprintID: int
    AtividadeDescricao: str
    AtividadeTipoID: str
    UsuarioChaveID: str
    AtividadeDataSolicitacao: Optional[str] = None
    UsuarioChave: str

class Planejado(SQLModel, table=True):
    ProjetoID: int = Field(primary_key=True)
    SprintID: int = Field(primary_key=True)
    AtividadeID: int = Field(primary_key=True)
    TempoEstimado: int
    PlanejamentoStatus: str
    UsuarioResponsavel: str

class Executado(SQLModel, table=True):
    ProjetoID: int = Field(primary_key=True)
    SprintID: int = Field(primary_key=True)
    AtividadeID: int = Field(primary_key=True)
    TempoReal: int
    AtividadeImpedidaData: Optional[str] = None
    AtividadeCanceladaData: Optional[str] = None
    AtividadeObservacao: Optional[str] = None
    UsuarioResponsavel: str
    AtividadeDataInicio: str
    AtividadeDataFim: str

class Usuario(SQLModel, table=True):
    UsuarioID: str = Field(primary_key=True)
    UsuarioNome: str
    UsuarioTipo: str 