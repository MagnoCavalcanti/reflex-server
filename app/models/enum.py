from enum import Enum


class TipoUsuario(str, Enum):
    aluno = "A"
    professor = "P"