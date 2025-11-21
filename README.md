# 🎓 Reflex Server - Backend da Plataforma de Cursos

## 📘 Sobre o Projeto

O **Reflex Server** é o backend de uma plataforma de ensino desenvolvida como projeto de extensão universitária. O sistema tem como objetivo **democratizar o acesso à educação em tecnologia**, permitindo que professores criem e gerenciem cursos gratuitamente, enquanto alunos podem se matricular e acompanhar seu progresso de aprendizado.

Este projeto foi desenvolvido utilizando **Python** e **FastAPI**, seguindo princípios de **Clean Architecture** e boas práticas de desenvolvimento, visando criar um sistema robusto, escalável e de fácil manutenção.

### 🎯 Objetivos

- ✅ Fornecer uma API REST completa e documentada
- ✅ Gerenciar autenticação segura de usuários (professores e alunos)
- ✅ Permitir criação e organização de cursos em módulos e aulas
- ✅ Suportar diferentes tipos de conteúdo (vídeos e quizzes interativos)
- ✅ Acompanhar progresso dos alunos
- ✅ Ser econômico e fácil de implantar

### 🏆 Contexto Acadêmico

Projeto desenvolvido para a disciplina de **Extensão P3** do curso de **Análise e Desenvolvimento de Sistemas** na **UNIFIP**, com entrega prevista para **novembro de 2025**.

## 🚀 Funcionalidades Principais

### 👤 Gestão de Usuários
- Cadastro de alunos e professores
- Autenticação segura com JWT
- Diferenciação de permissões por tipo de usuário

### 📚 Gestão de Cursos
- Criação de cursos por professores
- Organização em módulos hierárquicos
- Aulas com conteúdo variado (vídeos e quizzes)
- Sistema de matrículas

### 📝 Sistema de Avaliação
- Quizzes interativos com múltipla escolha
- Validação automática de respostas
- Cálculo de notas em porcentagem
- Prevenção de respostas duplicadas

### 📊 Acompanhamento de Progresso
- Marcação de aulas concluídas
- Marcação de módulos concluídos
- Histórico de tentativas em quizzes
- Dashboard de progresso do aluno

## 🛠️ Tecnologias Utilizadas

### Core
- **Python 3.12** - Linguagem de programação
- **FastAPI** - Framework web moderno e de alta performance
- **Pydantic** - Validação de dados e serialização
- **SQLAlchemy** - ORM para banco de dados
- **PostgreSQL** - Banco de dados relacional

### Segurança
- **JWT (JSON Web Tokens)** - Autenticação stateless
- **Passlib** - Hash seguro de senhas (bcrypt)
- **Python-JOSE** - Geração e validação de tokens

### DevOps
- **Docker** - Containerização
- **Docker Compose** - Orquestração de containers
- **Alembic** - Migrations de banco de dados
- **Uvicorn** - Servidor ASGI de produção

## 🏗️ Arquitetura do Projeto

O projeto segue uma **arquitetura em camadas** inspirada em **Clean Architecture** e **DDD (Domain-Driven Design)**:

```
reflex-server/
│
├── app/
│   ├── main.py                     # Ponto de entrada da aplicação FastAPI
│   │
│   ├── core/                       # 🔧 Configurações centrais
│   │   ├── db_connection.py        # Conexão com PostgreSQL
│   │   └── __init__.py
│   │
│   ├── models/                     # 🗄️ Modelos do banco de dados (SQLAlchemy ORM)
│   │   ├── base.py                 # Classe Base declarativa
│   │   ├── models.py               # User, Course, Module, Lesson, Quiz, etc.
│   │   └── enum.py                 # Enums (TipoUsuario)
│   │
│   ├── schemas/                    # 📋 Validação de dados (Pydantic)
│   │   ├── User.py                 # Schema de usuário
│   │   ├── Course.py               # Schema de curso
│   │   ├── Module.py               # Schema de módulo
│   │   ├── Lesson.py               # Schema de aula (vídeo e quiz)
│   │   └── __init__.py
│   │
│   ├── repositories/               # 💼 Lógica de negócio (Use Cases)
│   │   ├── auth_repo.py            # Autenticação (login, register)
│   │   ├── course_repo.py          # Gestão de cursos
│   │   ├── module_repo.py          # Gestão de módulos
│   │   ├── lesson_repo.py          # Gestão de aulas e quizzes
│   │   ├── user_repo.py            # Operações de usuário
│   │   └── __init__.py
│   │
│   ├── routers/                    # 🛣️ Endpoints da API (Controllers)
│   │   ├── auth_router.py          # POST /auth/register, /auth/login
│   │   ├── course_router.py        # GET/POST /courses
│   │   ├── module_router.py        # GET/POST /modules
│   │   ├── lesson_router.py        # GET/POST /lessons, /lessons/quiz
│   │   └── __init__.py
│   │
│   └── utils/                      # 🔨 Utilitários e helpers
│       ├── dependencies.py         # Injeção de dependências (DB, Auth)
│       └── __init__.py
│
├── migrations/                     # 📦 Migrations do Alembic
│   ├── versions/                   # Histórico de alterações no banco
│   └── env.py                      # Configuração do Alembic
│
├── .env                            # 🔐 Variáveis de ambiente (não commitado)
├── .dockerignore                   # Arquivos ignorados no build Docker
├── alembic.ini                     # Configuração do Alembic
├── docker-compose.yml              # Orquestração de containers
├── Dockerfile                      # Imagem Docker da aplicação
├── entrypoint.sh                   # Script de inicialização do container
├── requirements.txt                # Dependências Python
├── API_DOCUMENTATION.md            # 📖 Documentação completa da API
└── README.md                       # Este arquivo
```

### 📐 Camadas da Arquitetura

```
┌─────────────────────────────────────────┐
│      Routers (Camada de Apresentação)   │  ← HTTP Endpoints
├─────────────────────────────────────────┤
│   Repositories (Camada de Aplicação)    │  ← Lógica de Negócio
├─────────────────────────────────────────┤
│  Models + Schemas (Camada de Domínio)   │  ← Entidades e Regras
├─────────────────────────────────────────┤
│  Core + Utils (Camada de Infraestrutura)│  ← DB, Config, Helpers
└─────────────────────────────────────────┘
```

## 🔐 Segurança e Autenticação

### Autenticação JWT
- **Tokens de acesso** com validade de 30 minutos
- **Bearer token** no header Authorization
- Geração de tokens no login com payload customizado

### Validações Robustas
- **Senhas**: Mínimo 8 caracteres, 1 maiúscula, 1 minúscula, 1 número
- **Email**: Validação de formato com regex
- **Telefone**: Formato brasileiro (XX) XXXXX-XXXX
- **Quizzes**: Exatamente uma resposta correta por pergunta

### Controle de Acesso
- **Professores**: Podem criar/editar apenas seus próprios cursos
- **Alunos**: Podem matricular-se e responder quizzes
- **Rotas protegidas**: Middleware `get_current_user` valida tokens
- **Prevenção de duplicação**: Matrícula, conclusão de aulas, respostas de quiz

### Boas Práticas
- ✅ Senhas hasheadas com bcrypt (SHA-256)
- ✅ Variáveis sensíveis no `.env`
- ✅ CORS configurado para permitir frontend
- ✅ Tratamento centralizado de exceções
- ✅ Validação em múltiplas camadas (Pydantic + SQLAlchemy)


## 🚦 Como Executar o Projeto

### 📋 Pré-requisitos

- Python 3.12+
- PostgreSQL 17
- Docker e Docker Compose (opcional, mas recomendado)
- Git

### 🐳 Opção 1: Docker (Recomendado)

1. **Clone o repositório**
```bash
git clone https://github.com/MagnoCavalcanti/reflex-server.git
cd reflex-server
```

2. **Configure as variáveis de ambiente**
```bash
# Já existe um .env configurado, mas você pode ajustar conforme necessário
```

3. **Suba os containers**
```bash
docker-compose up --build
```

4. **Acesse a aplicação**
- API: http://localhost:8000
- Documentação interativa: http://localhost:8000/docs
- Banco de dados: localhost:5431

### 💻 Opção 2: Ambiente Local

1. **Clone e entre no diretório**
```bash
git clone https://github.com/MagnoCavalcanti/reflex-server.git
cd reflex-server
```

2. **Crie e ative ambiente virtual**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

4. **Configure o .env**
```env
DB_URL=postgresql://postgres:1407@localhost:5432/reflex_db
SECRET_KEY=sua_chave_secreta_aqui
ALGORITHM=HS256
```

5. **Execute as migrations**
```bash
alembic upgrade head
```

6. **Rode o servidor**
```bash
uvicorn app.main:app --reload
```

7. **Acesse a documentação**
```
http://localhost:8000/docs
```

## 📖 Documentação da API

A documentação completa de todos os endpoints está disponível em:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Arquivo Markdown**: [API_DOCUMENTATION.md](API_DOCUMENTATION.md)

### Principais Endpoints

| Método | Endpoint | Descrição | Auth |
|--------|----------|-----------|------|
| POST | `/auth/register` | Cadastro de usuário | ❌ |
| POST | `/auth/login` | Login e geração de token | ❌ |
| GET | `/courses/` | Lista todos os cursos | ❌ |
| POST | `/courses/` | Cria novo curso | ❌ |
| POST | `/courses/enrollments` | Matricula em um curso | ✅ |
| GET | `/modules/` | Lista todos os módulos | ❌ |
| POST | `/modules/` | Cria módulo (professor) | ✅ |
| POST | `/modules/{id}` | Completa módulo | ✅ |
| GET | `/lessons/` | Lista todas as aulas | ❌ |
| POST | `/lessons/` | Cria aula (professor) | ✅ |
| POST | `/lessons/create/video` | Adiciona vídeo à aula | ✅ |
| POST | `/lessons/create/quiz` | Cria quiz | ✅ |
| POST | `/lessons/quiz/answer` | Responde quiz | ✅ |

## 🧪 Testes

### Testando com Swagger
```
1. Acesse http://localhost:8000/docs
2. Clique em "Authorize" e cole o token JWT
3. Teste os endpoints diretamente na interface
```

### Exemplos com cURL

**Registrar usuário:**
```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "maria",
    "password": "Maria123",
    "email": "maria@example.com",
    "fullname": "Maria Santos",
    "telephone": "(11) 98765-4321",
    "type_user": "A"
  }'
```

**Login:**
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=maria&password=Maria123"
```

## 🤝 Como Contribuir

### Padrões de Branch
- `feature/nome-funcionalidade` - Novas funcionalidades
- `fix/descricao-do-bug` - Correções de bugs
- `docs/atualizacao` - Atualizações de documentação
- `refactor/melhoria` - Refatorações de código

### Padrões de Commit
Seguimos o [Conventional Commits](https://www.conventionalcommits.org/):

```bash
feat: adicionar endpoint de criação de curso
fix: corrigir validação do email do usuário
docs: atualizar README com instruções Docker
refactor: reorganizar estrutura de pastas
test: adicionar testes para auth_router
```

### Fluxo de Trabalho
1. Crie uma branch a partir da `main`
2. Desenvolva e commit suas alterações
3. Teste localmente
4. Abra um Pull Request
5. Aguarde code review

## 📊 Modelo de Dados

### Principais Entidades

```mermaid
erDiagram
    USER ||--o{ COURSE : creates
    USER ||--o{ COURSE_ENROLLMENT : enrolls
    COURSE ||--o{ MODULE : contains
    MODULE ||--o{ LESSON : contains
    LESSON ||--o{ LESSON_VIDEO : has
    LESSON ||--o{ LESSON_QUIZ : has
    LESSON_QUIZ ||--o{ QUIZ_QUESTION : has
    QUIZ_QUESTION ||--o{ QUIZ_OPTION : has
```

## 👥 Equipe

**Desenvolvedor Principal**: [Seu Nome]  
**Orientador**: [Nome do Orientador]  
**Universidade**: [Nome da Universidade]  
**Curso**: [Seu Curso]  
**Período**: 2025.2

## 📝 Licença

Este projeto é desenvolvido para fins acadêmicos como parte do projeto de extensão universitária.


---

**Desenvolvido com ❤️ para democratizar o ensino de tecnologia**
