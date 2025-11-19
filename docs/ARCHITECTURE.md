# 🏗️ Arquitetura do Projeto - Reflex Server

## 📋 Visão Geral

Este projeto segue uma **arquitetura em camadas** (Layered Architecture) inspirada nos princípios de **Clean Architecture** e **Domain-Driven Design (DDD)**. A separação de responsabilidades garante código mais organizado, testável e escalável.

---

## 📁 Estrutura de Diretórios

```
app/
├── main.py                 # Ponto de entrada da aplicação
├── core/                   # Configurações centrais
├── models/                 # Entidades do banco de dados
├── schemas/                # Validação e serialização
├── repositories/           # Lógica de negócio
├── routers/                # Endpoints HTTP
└── utils/                  # Utilitários e helpers
```

---

## 🎯 Camadas da Arquitetura

### **Camada de Apresentação** → `routers/`
- **Responsabilidade**: Interface com o cliente (HTTP)
- **Função**: Receber requisições e retornar respostas

### **Camada de Aplicação** → `repositories/`
- **Responsabilidade**: Casos de uso e regras de negócio
- **Função**: Orquestrar operações e validações

### **Camada de Domínio** → `models/` + `schemas/`
- **Responsabilidade**: Entidades e contratos de dados
- **Função**: Definir estrutura e validação dos dados

### **Camada de Infraestrutura** → `core/` + `utils/`
- **Responsabilidade**: Recursos externos (DB, config)
- **Função**: Gerenciar conexões e dependências

---

## 📂 Módulos Detalhados

### 📄 **main.py** - Ponto de Entrada

**Responsabilidade**: Inicializar e configurar a aplicação FastAPI

```python
from fastapi import FastAPI
from app.routers import auth_router

app = FastAPI(title="Reflex Server API")
app.include_router(auth_router)
```

**Funções**:
- ✅ Criar instância do FastAPI
- ✅ Registrar routers (blueprints de rotas)
- ✅ Configurar CORS, middlewares
- ✅ Definir documentação automática (Swagger/OpenAPI)

**Quando modificar**: Adicionar novos routers ou configurações globais

---

### 📁 **core/** - Núcleo da Aplicação

#### 📄 **db_connection.py**

**Responsabilidade**: Gerenciar conexão com banco de dados

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = config("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
```

**Funções**:
- ✅ Criar engine do SQLAlchemy
- ✅ Configurar pool de conexões
- ✅ Definir SessionLocal para transações

**Padrão**: Singleton Pattern (uma única engine)

**Quando modificar**: Mudar banco de dados ou configurações de conexão

---

### 📁 **models/** - Modelos de Dados (ORM)

#### 📄 **base.py**

**Responsabilidade**: Classe base para todos os modelos

```python
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
```

**Funções**:
- ✅ Fornecer classe base para herança
- ✅ Registrar metadados das tabelas

---

#### 📄 **models.py**

**Responsabilidade**: Definir entidades do domínio como tabelas SQL

```python
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
```

**Funções**:
- ✅ Mapear classes Python → Tabelas SQL (ORM)
- ✅ Definir colunas, tipos e constraints
- ✅ Estabelecer relacionamentos (ForeignKey)

**Entidades Disponíveis**:
- `User` - Usuários do sistema
- `Course` - Cursos disponíveis
- `Module` - Módulos dos cursos
- `Lesson` - Aulas dos módulos
- `CourseEnrollment` - Matrículas em cursos

**Padrão**: Active Record Pattern (ORM)

**Quando modificar**: Adicionar novas tabelas ou alterar estrutura do banco

---

### 📁 **schemas/** - Validação de Dados (DTOs)

#### 📄 **User.py**

**Responsabilidade**: Schema para criação/leitura de usuários

```python
from pydantic import BaseModel, EmailStr

class User(BaseModel):
    username: str
    email: EmailStr
    password: str
    fullname: str | None
    telephone: str | None
```

**Funções**:
- ✅ Validar tipos de dados (Pydantic)
- ✅ Serializar/Deserializar JSON ↔ Python
- ✅ Documentação automática da API
- ✅ Garantir contratos de entrada/saída

---

#### 📄 **UserLogin.py**

**Responsabilidade**: Schema específico para autenticação

```python
class UserLogin(BaseModel):
    username: str
    password: str
```

**Funções**:
- ✅ Validar credenciais de login
- ✅ Manter apenas campos necessários (princípio do menor privilégio)

**Padrão**: Data Transfer Object (DTO)

**Quando modificar**: Adicionar novos endpoints com diferentes estruturas de dados

---

### 📁 **repositories/** - Lógica de Negócio

#### 📄 **auth_repo.py**

**Responsabilidade**: Casos de uso relacionados à autenticação

```python
class AuthUseCases:
    def __init__(self, db_session: Session):
        self.db = db_session
    
    def register(self, user: UserSchema):
        # Hash da senha + salvar no banco
    
    def login(self, user: UserLogin):
        # Validar credenciais + gerar JWT token
    
    def verify_token(self, token: str):
        # Validar token JWT
```

**Funções**:
- ✅ **register()**: Cadastrar novo usuário com senha hasheada
- ✅ **login()**: Autenticar e gerar token JWT
- ✅ **verify_token()**: Validar tokens de acesso

**Responsabilidades**:
- 🔐 Hash de senhas (bcrypt/passlib)
- 🎫 Geração e validação de JWT
- 🗃️ Operações no banco de dados
- ⚠️ Tratamento de erros (HTTPException)

**Padrão**: Repository Pattern + Use Case Pattern

**Quando modificar**: Adicionar novos casos de uso (ex: recuperar senha, refresh token)

---

### 📁 **routers/** - Endpoints da API

#### 📄 **auth_router.py**

**Responsabilidade**: Definir rotas HTTP de autenticação

```python
auth_router = APIRouter(prefix="/auth")

@auth_router.post("/register")
def register(user: UserSchema, db: Session = Depends(get_db_session)):
    auth_uc = AuthUseCases(db)
    auth_uc.register(user)
    return JSONResponse({"msg": "success"}, status_code=201)

@auth_router.post("/login")
def login(form: OAuth2PasswordRequestForm = Depends(), 
          db: Session = Depends(get_db_session)):
    auth_uc = AuthUseCases(db)
    user = UserLogin(username=form.username, password=form.password)
    token_data = auth_uc.login(user)
    return JSONResponse(token_data, status_code=200)
```

**Funções**:
- ✅ Definir endpoints (POST, GET, PUT, DELETE)
- ✅ Injetar dependências (DB session)
- ✅ Chamar repositórios
- ✅ Retornar respostas HTTP padronizadas

**Rotas Disponíveis**:
- `POST /auth/register` - Cadastro de usuário
- `POST /auth/login` - Login e geração de token

**Padrão**: Controller Pattern (MVC)

**Quando modificar**: Adicionar novos endpoints ou modificar comportamento das rotas

---

### 📁 **utils/** - Utilitários

#### 📄 **dependencies.py**

**Responsabilidade**: Funções auxiliares e injeção de dependências

```python
def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

**Funções**:
- ✅ **get_db_session()**: Fornece sessão do banco de dados
- ✅ Garantir fechamento da sessão (context manager)
- ✅ Reutilização via `Depends()`

**Padrão**: Dependency Injection

**Quando modificar**: Adicionar novos helpers compartilhados

---

## 🔄 Fluxo Completo de uma Requisição

```
1. Cliente HTTP
   └─> POST /auth/register {"username": "john", "password": "123"}
         │
2. main.py (FastAPI)
   └─> Roteia para auth_router
         │
3. routers/auth_router.py
   └─> Valida dados com schemas/User.py (Pydantic)
   └─> Injeta dependência: utils/get_db_session()
         │
4. repositories/auth_repo.py (AuthUseCases)
   └─> Executa lógica de negócio:
       - Hash da senha (passlib)
       - Cria instância de models/User
       - Salva no banco via SQLAlchemy
         │
5. core/db_connection.py
   └─> Gerencia transação com banco de dados
         │
6. Resposta HTTP
   └─> {"msg": "success"} com status 201
```

---

## 🎨 Princípios de Design Aplicados

### ✅ **Single Responsibility Principle (SRP)**
Cada módulo tem uma única responsabilidade:
- Routers → HTTP
- Repositories → Lógica de negócio
- Models → Estrutura de dados

### ✅ **Dependency Inversion Principle (DIP)**
Camadas superiores dependem de abstrações, não de implementações:
- Routers recebem `Session` via injeção de dependência
- Repositories trabalham com interfaces (schemas)

### ✅ **Separation of Concerns (SoC)**
Separação clara entre:
- Apresentação (routers)
- Aplicação (repositories)
- Domínio (models/schemas)
- Infraestrutura (core/utils)

### ✅ **Don't Repeat Yourself (DRY)**
Código reutilizável em `utils/` e `core/`

---

## 📚 Tecnologias Utilizadas

| Camada | Tecnologia | Propósito |
|--------|-----------|-----------|
| Framework | FastAPI | API REST moderna e rápida |
| ORM | SQLAlchemy | Mapeamento objeto-relacional |
| Validação | Pydantic | Validação de dados |
| Autenticação | JWT + Passlib | Tokens seguros e hash de senhas |
| Banco de Dados | PostgreSQL/SQLite | Persistência de dados |

---

## 🚀 Como Estender o Projeto

### Adicionar novo recurso (ex: Cursos):

1. **Criar schema** em `schemas/Course.py`
2. **Criar repository** em `repositories/course_repo.py`
3. **Criar router** em `routers/course_router.py`
4. **Registrar router** em `main.py`
5. **Modelo já existe** em `models/models.py`

### Adicionar autenticação a uma rota:

```python
from fastapi import Depends
from utils.dependencies import get_current_user

@router.get("/protected")
def protected_route(current_user: User = Depends(get_current_user)):
    return {"user": current_user.username}
```

---