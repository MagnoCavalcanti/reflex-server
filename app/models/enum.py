from enum import Enum


class TipoUsuario(str, Enum):
    aluno = "A"
    professor = "P"

class ContentType(str, Enum):
    video = "V"
    quiz = "Q"