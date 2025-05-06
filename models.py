from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import date, datetime
from pydantic import BaseModel, ConfigDict

class Projeto(SQLModel, table=True):
    ProjetoID: int = Field(default=None, primary_key=True)
    Nome: str
    DataInicio: str
    DataFim: str
    GerenteProjeto: str
    SolicitanteProjeto: str

    # Relationship to Sprint
    sprints: List["Sprint"] = Relationship(
        back_populates="projeto",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
    atividades: List["Atividade"] = Relationship(
        back_populates="projeto",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )

class Sprint(SQLModel, table=True):
    SprintID: int = Field(default=None, primary_key=True)
    ProjetoID: int = Field(foreign_key="projeto.ProjetoID")
    SprintNome: str
    SprintDataInicio: str
    SprintDataFim: str

    # Relationship to Atividade
    tasks: List["Atividade"] = Relationship(
        back_populates="sprint",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
    projeto: Optional["Projeto"] = Relationship(back_populates="sprints")

class Atividade(SQLModel, table=True):
    AtividadeID: int = Field(default=None, primary_key=True)
    ProjetoID: int = Field(foreign_key="projeto.ProjetoID")
    SprintID: int = Field(foreign_key="sprint.SprintID")
    AtividadeDescricao: str
    AtividadeTipo: str
    AtividadeDataSolicitacao: Optional[str] = None
    UsuarioChave: str
    TempoEstimado: int
    UsuarioResponsavel: str

    # Relationships
    sprint: Optional["Sprint"] = Relationship(back_populates="tasks")
    projeto: Optional["Projeto"] = Relationship(back_populates="atividades")

class Executado(SQLModel, table=True):
    ExecutadoID: int = Field(default=None, primary_key=True)
    AtividadeID: int = Field(foreign_key="atividade.AtividadeID")
    ProjetoID: int = Field(foreign_key="projeto.ProjetoID")
    SprintID: int = Field(foreign_key="sprint.SprintID")
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

class AtividadeRead(BaseModel):
    AtividadeID: int
    ProjetoID: int
    SprintID: int
    AtividadeDescricao: str
    AtividadeTipo: str
    AtividadeDataSolicitacao: Optional[str] = None
    UsuarioChave: str
    TempoEstimado: int
    UsuarioResponsavel: str

    @classmethod
    def from_orm(cls, obj):
        return cls(
            AtividadeID=obj.AtividadeID,
            ProjetoID=obj.ProjetoID,
            SprintID=obj.SprintID,
            AtividadeDescricao=obj.AtividadeDescricao,
            AtividadeTipo=obj.AtividadeTipo,
            AtividadeDataSolicitacao=obj.AtividadeDataSolicitacao,
            UsuarioChave=obj.UsuarioChave,
            TempoEstimado=obj.TempoEstimado,
            UsuarioResponsavel=obj.UsuarioResponsavel
        )

    model_config = ConfigDict(from_attributes=True)

class SprintRead(BaseModel):
    SprintID: int
    ProjetoID: int
    SprintNome: str
    SprintDataInicio: str
    SprintDataFim: str
    tasks: List[AtividadeRead] = []

    @classmethod
    def from_orm(cls, obj):
        return cls(
            SprintID=obj.SprintID,
            ProjetoID=obj.ProjetoID,
            SprintNome=obj.SprintNome,
            SprintDataInicio=obj.SprintDataInicio,
            SprintDataFim=obj.SprintDataFim,
            tasks=[AtividadeRead.from_orm(task) for task in obj.tasks]
        )

    model_config = ConfigDict(from_attributes=True)

class ProjetoRead(BaseModel):
    ProjetoID: int
    Nome: str
    DataInicio: str
    DataFim: str
    GerenteProjeto: str
    SolicitanteProjeto: str
    sprints: List[SprintRead] = []
    atividades: List[AtividadeRead] = []

    @classmethod
    def from_orm(cls, obj):
        return cls(
            ProjetoID=obj.ProjetoID,
            Nome=obj.Nome,
            DataInicio=obj.DataInicio,
            DataFim=obj.DataFim,
            GerenteProjeto=obj.GerenteProjeto,
            SolicitanteProjeto=obj.SolicitanteProjeto,
            sprints=[SprintRead.from_orm(sprint) for sprint in obj.sprints],
            atividades=[AtividadeRead.from_orm(atividade) for atividade in obj.atividades]
        )

    model_config = ConfigDict(from_attributes=True) 