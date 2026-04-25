# 🔗 Documentação de Rotas - Para o Time Frontend

**Base URL:** `http://localhost:8000`

---

## 📋 Índice
1. [Autenticação](#autenticação)
2. [Cursos](#cursos)
3. [Módulos](#módulos)
4. [Aulas e Quizzes](#aulas-e-quizzes)

---

## 🔐 Autenticação

### 1. Registrar Novo Usuário

**Endpoint:** `POST /auth/register`

**Autenticação:** ❌ Não requer

**Content-Type:** `application/json`

**Body (JSON):**
```json
{
  "username": "maria_silva",
  "password": "Senha123",
  "email": "maria@example.com",
  "fullname": "Maria da Silva",
  "telephone": "(11) 98765-4321",
  "type_user": "A"
}
```

**Parâmetros:**
| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| `username` | string | ✅ Sim | Nome de usuário único |
| `password` | string | ✅ Sim | Mínimo 8 caracteres, 1 maiúscula, 1 minúscula, 1 número |
| `email` | string | ✅ Sim | Email válido (formato: usuario@dominio.com) |
| `fullname` | string | ✅ Sim | Nome completo do usuário |
| `telephone` | string | ✅ Sim | Telefone no formato (XX) XXXXX-XXXX |
| `type_user` | string | ✅ Sim | `"A"` para aluno ou `"P"` para professor |

**Resposta Esperada (201 Created):**
```json
{
  "msg": "sucess"
}
```

**Possíveis Erros:**

| Status | Erro | Descrição |
|--------|------|-----------|
| 422 | Email inválido | Formato de email incorreto |
| 422 | Senha deve ter no mínimo 8 caracteres | Senha muito curta |
| 422 | Senha deve conter pelo menos uma letra maiúscula | Falta maiúscula |
| 422 | Senha deve conter pelo menos uma letra minúscula | Falta minúscula |
| 422 | Senha deve conter pelo menos um número | Falta número |
| 422 | Telefone deve estar no formato | Formato de telefone incorreto |
| 422 | Tipo de usuário inválido | Use 'A' ou 'P' |
| 400 | Usuário já existe | Username ou email duplicado |

**Exemplo com cURL:**
```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "maria_silva",
    "password": "Senha123",
    "email": "maria@example.com",
    "fullname": "Maria da Silva",
    "telephone": "(11) 98765-4321",
    "type_user": "A"
  }'
```

---

### 2. Fazer Login

**Endpoint:** `POST /auth/login`

**Autenticação:** ❌ Não requer

**Content-Type:** `application/x-www-form-urlencoded`

**Body (Form Data):**
```
username=maria_silva&password=Senha123
```

**Parâmetros:**
| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| `username` | string | ✅ Sim | Nome de usuário |
| `password` | string | ✅ Sim | Senha |

**Resposta Esperada (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user_id": 1,
  "username": "maria_silva",
  "type_user": "A"
}
```

**Como usar o Token:**
Adicione o token no header de todas as requisições autenticadas:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Possíveis Erros:**

| Status | Erro | Descrição |
|--------|------|-----------|
| 401 | Credenciais inválidas | Username ou senha incorretos |
| 400 | Usuário não encontrado | Username não existe |

**Exemplo com cURL:**
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=maria_silva&password=Senha123"
```

**Exemplo com JavaScript (Fetch):**
```javascript
const formData = new FormData();
formData.append('username', 'maria_silva');
formData.append('password', 'Senha123');

const response = await fetch('http://localhost:8000/auth/login', {
  method: 'POST',
  body: formData
});

const data = await response.json();
console.log(data.access_token);
// Guardar em localStorage
localStorage.setItem('token', data.access_token);
```

---

## 📚 Cursos

### 3. Listar Todos os Cursos

**Endpoint:** `GET /courses/`

**Autenticação:** ❌ Não requer

**Resposta Esperada (200 OK):**
```json
[
  {
    "id": 1,
    "title": "Python Avançado",
    "description": "Aprenda técnicas avançadas de Python",
    "professor_id": 1,
    "created_at": "2025-04-20T10:30:00",
    "updated_at": "2025-04-20T10:30:00"
  },
  {
    "id": 2,
    "title": "Web Development com FastAPI",
    "description": "Desenvolva APIs modernas com FastAPI",
    "professor_id": 2,
    "created_at": "2025-04-21T14:15:00",
    "updated_at": "2025-04-21T14:15:00"
  }
]
```

**Possíveis Erros:**

| Status | Erro | Descrição |
|--------|------|-----------|
| 500 | Internal Server Error | Erro ao conectar com banco de dados |

**Exemplo com cURL:**
```bash
curl -X GET "http://localhost:8000/courses/"
```

**Exemplo com JavaScript:**
```javascript
const response = await fetch('http://localhost:8000/courses/');
const courses = await response.json();
console.log(courses);
```

---

### 4. Criar Novo Curso

**Endpoint:** `POST /courses/`

**Autenticação:** ✅ Requer (Token JWT)

**Content-Type:** `application/json`

**Body (JSON):**
```json
{
  "title": "React Fundamentals",
  "description": "Aprenda os fundamentos do React",
  "professor_id": 1
}
```

**Parâmetros:**
| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| `title` | string | ✅ Sim | Título do curso |
| `description` | string | ✅ Sim | Descrição do curso |
| `professor_id` | integer | ✅ Sim | ID do professor que criará o curso |

**Resposta Esperada (201 Created):**
```json
{
  "message": "Curso criado com sucesso."
}
```

**Possíveis Erros:**

| Status | Erro | Descrição |
|--------|------|-----------|
| 401 | Unauthorized | Token ausente ou inválido |
| 422 | Unprocessable Entity | Dados inválidos ou incompletos |
| 403 | Forbidden | Apenas professores podem criar cursos |

**Exemplo com cURL:**
```bash
curl -X POST "http://localhost:8000/courses/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer seu_token_aqui" \
  -d '{
    "title": "React Fundamentals",
    "description": "Aprenda os fundamentos do React",
    "professor_id": 1
  }'
```

**Exemplo com JavaScript:**
```javascript
const token = localStorage.getItem('token');

const response = await fetch('http://localhost:8000/courses/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  },
  body: JSON.stringify({
    title: "React Fundamentals",
    description: "Aprenda os fundamentos do React",
    professor_id: 1
  })
});

const data = await response.json();
console.log(data);
```

---

### 5. Matricular em um Curso

**Endpoint:** `POST /courses/enrollments`

**Autenticação:** ✅ Requer (Token JWT)

**Query Parameters:**
| Parâmetro | Tipo | Obrigatório | Descrição |
|-----------|------|-------------|-----------|
| `course_id` | integer | ✅ Sim | ID do curso |

**Body:** Vazio (enviar `{}` ou sem body)

**Resposta Esperada (201 Created):**
```json
{
  "msg": "success"
}
```

**Possíveis Erros:**

| Status | Erro | Descrição |
|--------|------|-----------|
| 401 | Unauthorized | Token ausente ou inválido |
| 404 | Not Found | Curso não existe |
| 400 | Bad Request | Aluno já está matriculado no curso |
| 403 | Forbidden | Apenas alunos podem se matricular |

**Exemplo com cURL:**
```bash
curl -X POST "http://localhost:8000/courses/enrollments?course_id=1" \
  -H "Authorization: Bearer seu_token_aqui"
```

**Exemplo com JavaScript:**
```javascript
const token = localStorage.getItem('token');
const courseId = 1;

const response = await fetch(`http://localhost:8000/courses/enrollments?course_id=${courseId}`, {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`
  }
});

const data = await response.json();
console.log(data);
```

---

## 📦 Módulos

### 6. Listar Todos os Módulos

**Endpoint:** `GET /modules/`

**Autenticação:** ❌ Não requer

**Resposta Esperada (200 OK):**
```json
[
  {
    "id": 1,
    "title": "Módulo 1 - Fundamentos",
    "course_id": 1,
    "created_at": "2025-04-20T10:30:00",
    "updated_at": "2025-04-20T10:30:00",
    "lessons": [
      {
        "id": 1,
        "title": "Aula 1 - Introdução",
        "content_type": "V"
      }
    ]
  }
]
```

**Exemplo com cURL:**
```bash
curl -X GET "http://localhost:8000/modules/"
```

---

### 7. Obter Módulo Específico

**Endpoint:** `GET /modules/{module_id}`

**Autenticação:** ❌ Não requer

**Path Parameters:**
| Parâmetro | Tipo | Obrigatório | Descrição |
|-----------|------|-------------|-----------|
| `module_id` | integer | ✅ Sim | ID do módulo |

**Resposta Esperada (200 OK):**
```json
{
  "id": 1,
  "title": "Módulo 1 - Fundamentos",
  "course_id": 1,
  "created_at": "2025-04-20T10:30:00",
  "updated_at": "2025-04-20T10:30:00",
  "lessons": [
    {
      "id": 1,
      "title": "Aula 1 - Introdução",
      "content_type": "V"
    }
  ]
}
```

**Possíveis Erros:**

| Status | Erro | Descrição |
|--------|------|-----------|
| 404 | Not Found | Módulo não existe |

**Exemplo com cURL:**
```bash
curl -X GET "http://localhost:8000/modules/1"
```

---

### 8. Criar Módulo

**Endpoint:** `POST /modules/`

**Autenticação:** ✅ Requer (Token JWT)

**Content-Type:** `application/json`

**Body (JSON):**
```json
{
  "title": "Módulo 2 - Avançado",
  "course_id": 1
}
```

**Parâmetros:**
| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| `title` | string | ✅ Sim | Título do módulo |
| `course_id` | integer | ✅ Sim | ID do curso |

**Resposta Esperada (201 Created):**
```json
{
  "msg": "success"
}
```

**Possíveis Erros:**

| Status | Erro | Descrição |
|--------|------|-----------|
| 401 | Unauthorized | Token ausente ou inválido |
| 403 | Forbidden | Apenas o professor do curso pode criar módulos |
| 404 | Not Found | Curso não existe |

**Exemplo com JavaScript:**
```javascript
const token = localStorage.getItem('token');

const response = await fetch('http://localhost:8000/modules/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  },
  body: JSON.stringify({
    title: "Módulo 2 - Avançado",
    course_id: 1
  })
});

const data = await response.json();
console.log(data);
```

---

### 9. Marcar Módulo como Concluído

**Endpoint:** `POST /modules/{module_id}`

**Autenticação:** ✅ Requer (Token JWT)

**Path Parameters:**
| Parâmetro | Tipo | Obrigatório | Descrição |
|-----------|------|-------------|-----------|
| `module_id` | integer | ✅ Sim | ID do módulo |

**Body:** Vazio (enviar `{}` ou sem body)

**Resposta Esperada (200 OK):**
```json
{
  "msg": "success"
}
```

**Possíveis Erros:**

| Status | Erro | Descrição |
|--------|------|-----------|
| 401 | Unauthorized | Token ausente ou inválido |
| 404 | Not Found | Módulo não existe |
| 400 | Bad Request | Módulo já foi concluído |

**Exemplo com JavaScript:**
```javascript
const token = localStorage.getItem('token');
const moduleId = 1;

const response = await fetch(`http://localhost:8000/modules/${moduleId}`, {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`
  }
});

const data = await response.json();
console.log(data);
```

---

## 📖 Aulas e Quizzes

### 10. Listar Todas as Aulas

**Endpoint:** `GET /lessons/`

**Autenticação:** ❌ Não requer

**Resposta Esperada (200 OK):**
```json
[
  {
    "id": 1,
    "title": "Aula 1 - Introdução",
    "content_type": "V",
    "module_id": 1,
    "created_at": "2025-04-20T10:30:00",
    "updated_at": "2025-04-20T10:30:00",
    "video": {
      "id": 1,
      "video_url": "https://youtube.com/watch?v=..."
    }
  },
  {
    "id": 2,
    "title": "Aula 2 - Quiz",
    "content_type": "Q",
    "module_id": 1,
    "created_at": "2025-04-21T14:00:00",
    "updated_at": "2025-04-21T14:00:00",
    "quiz": {
      "id": 1,
      "questions": []
    }
  }
]
```

**Exemplo com cURL:**
```bash
curl -X GET "http://localhost:8000/lessons/"
```

---

### 11. Obter Aula Específica

**Endpoint:** `GET /lessons/{lesson_id}`

**Autenticação:** ❌ Não requer

**Path Parameters:**
| Parâmetro | Tipo | Obrigatório | Descrição |
|-----------|------|-------------|-----------|
| `lesson_id` | integer | ✅ Sim | ID da aula |

**Resposta Esperada (200 OK):**
```json
{
  "id": 1,
  "title": "Aula 1 - Introdução",
  "content_type": "V",
  "module_id": 1,
  "created_at": "2025-04-20T10:30:00",
  "updated_at": "2025-04-20T10:30:00",
  "video": {
    "id": 1,
    "video_url": "https://youtube.com/watch?v=..."
  }
}
```

**Possíveis Erros:**

| Status | Erro | Descrição |
|--------|------|-----------|
| 404 | Not Found | Aula não existe |

---

### 12. Criar Aula

**Endpoint:** `POST /lessons/`

**Autenticação:** ✅ Requer (Token JWT)

**Content-Type:** `application/json`

**Body (JSON):**
```json
{
  "title": "Aula 3 - Práticas",
  "content_type": "V",
  "module_id": 1
}
```

**Parâmetros:**
| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| `title` | string | ✅ Sim | Título da aula |
| `content_type` | string | ✅ Sim | `"V"` para vídeo ou `"Q"` para quiz |
| `module_id` | integer | ✅ Sim | ID do módulo |

**Resposta Esperada (201 Created):**
```json
{
  "msg": "success",
  "id": 3
}
```

**Possíveis Erros:**

| Status | Erro | Descrição |
|--------|------|-----------|
| 401 | Unauthorized | Token ausente ou inválido |
| 422 | Unprocessable Entity | content_type deve ser "V" ou "Q" |
| 403 | Forbidden | Apenas professores podem criar aulas |

**Exemplo com JavaScript:**
```javascript
const token = localStorage.getItem('token');

const response = await fetch('http://localhost:8000/lessons/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  },
  body: JSON.stringify({
    title: "Aula 3 - Práticas",
    content_type: "V",
    module_id: 1
  })
});

const data = await response.json();
console.log(data.id);
```

---

### 13. Adicionar Vídeo à Aula

**Endpoint:** `POST /lessons/create/video`

**Autenticação:** ✅ Requer (Token JWT)

**Content-Type:** `application/json`

**Body (JSON):**
```json
{
  "lesson_id": 1,
  "video_url": "https://youtube.com/watch?v=dQw4w9WgXcQ"
}
```

**Parâmetros:**
| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| `lesson_id` | integer | ✅ Sim | ID da aula |
| `video_url` | string | ✅ Sim | URL do vídeo |

**Resposta Esperada (201 Created):**
```json
{
  "msg": "success"
}
```

**Possíveis Erros:**

| Status | Erro | Descrição |
|--------|------|-----------|
| 401 | Unauthorized | Token ausente ou inválido |
| 404 | Not Found | Aula não existe |
| 403 | Forbidden | Apenas o professor pode adicionar vídeos |

**Exemplo com JavaScript:**
```javascript
const token = localStorage.getItem('token');

const response = await fetch('http://localhost:8000/lessons/create/video', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  },
  body: JSON.stringify({
    lesson_id: 1,
    video_url: "https://youtube.com/watch?v=dQw4w9WgXcQ"
  })
});

const data = await response.json();
console.log(data);
```

---

### 14. Marcar Aula como Concluída

**Endpoint:** `POST /lessons/{lesson_id}`

**Autenticação:** ✅ Requer (Token JWT)

**Path Parameters:**
| Parâmetro | Tipo | Obrigatório | Descrição |
|-----------|------|-------------|-----------|
| `lesson_id` | integer | ✅ Sim | ID da aula |

**Body:** Vazio (enviar `{}` ou sem body)

**Resposta Esperada (200 OK):**
```json
{
  "msg": "success"
}
```

**Possíveis Erros:**

| Status | Erro | Descrição |
|--------|------|-----------|
| 401 | Unauthorized | Token ausente ou inválido |
| 404 | Not Found | Aula não existe |
| 400 | Bad Request | Aula já foi concluída |

**Exemplo com JavaScript:**
```javascript
const token = localStorage.getItem('token');
const lessonId = 1;

const response = await fetch(`http://localhost:8000/lessons/${lessonId}`, {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`
  }
});

const data = await response.json();
console.log(data);
```

---

## 🎯 Quiz

### 15. Criar Quiz em uma Aula

**Endpoint:** `POST /lessons/create/quiz`

**Autenticação:** ✅ Requer (Token JWT)

**Content-Type:** `application/json`

**Body (JSON):**
```json
{
  "lesson_id": 2,
  "questions": [
    {
      "quiz_id": 1,
      "question_text": "Qual é a capital do Brasil?",
      "options": [
        {
          "question_id": 1,
          "option_text": "São Paulo",
          "is_correct": false
        },
        {
          "question_id": 1,
          "option_text": "Brasília",
          "is_correct": true
        },
        {
          "question_id": 1,
          "option_text": "Rio de Janeiro",
          "is_correct": false
        }
      ]
    }
  ]
}
```

**Parâmetros:**
| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| `lesson_id` | integer | ✅ Sim | ID da aula |
| `questions` | array | ✅ Sim | Lista de perguntas |
| `questions[].quiz_id` | integer | ✅ Sim | ID do quiz |
| `questions[].question_text` | string | ✅ Sim | Texto da pergunta |
| `questions[].options` | array | ✅ Sim | Lista de opções |
| `options[].question_id` | integer | ✅ Sim | ID da pergunta |
| `options[].option_text` | string | ✅ Sim | Texto da opção |
| `options[].is_correct` | boolean | ❌ Não | Se é a resposta correta (padrão: false) |

**Resposta Esperada (201 Created):**
```json
{
  "msg": "success"
}
```

**Possíveis Erros:**

| Status | Erro | Descrição |
|--------|------|-----------|
| 401 | Unauthorized | Token ausente ou inválido |
| 404 | Not Found | Aula não existe |
| 403 | Forbidden | Apenas professores podem criar quizzes |

**Nota Importante:** ⚠️ Cada pergunta deve ter **exatamente uma opção correta**.

---

### 16. Obter Perguntas do Quiz

**Endpoint:** `GET /lessons/quiz/questions`

**Autenticação:** ❌ Não requer

**Query Parameters:**
| Parâmetro | Tipo | Obrigatório | Descrição |
|-----------|------|-------------|-----------|
| `quiz_id` | integer | ✅ Sim | ID do quiz |

**Resposta Esperada (200 OK):**
```json
[
  {
    "id": 1,
    "quiz_id": 1,
    "question_text": "Qual é a capital do Brasil?",
    "options": [
      {
        "id": 1,
        "question_id": 1,
        "option_text": "São Paulo",
        "is_correct": false
      },
      {
        "id": 2,
        "question_id": 1,
        "option_text": "Brasília",
        "is_correct": true
      },
      {
        "id": 3,
        "question_id": 1,
        "option_text": "Rio de Janeiro",
        "is_correct": false
      }
    ]
  }
]
```

**Nota Importante:** ⚠️ A resposta correta **NÃO** é revelada. O campo `is_correct` retorna como `false` para todas as opções. Use apenas para exibir o quiz no frontend.

**Exemplo com cURL:**
```bash
curl -X GET "http://localhost:8000/lessons/quiz/questions?quiz_id=1"
```

**Exemplo com JavaScript:**
```javascript
const quizId = 1;

const response = await fetch(`http://localhost:8000/lessons/quiz/questions?quiz_id=${quizId}`);
const questions = await response.json();
console.log(questions);
```

---

### 17. Adicionar Pergunta ao Quiz

**Endpoint:** `POST /lessons/quiz/question`

**Autenticação:** ✅ Requer (Token JWT)

**Content-Type:** `application/json`

**Body (JSON):**
```json
{
  "quiz_id": 1,
  "question_text": "Qual linguagem é usada para estilizar web?",
  "options": [
    {
      "question_id": 2,
      "option_text": "Python",
      "is_correct": false
    },
    {
      "question_id": 2,
      "option_text": "CSS",
      "is_correct": true
    },
    {
      "question_id": 2,
      "option_text": "JavaScript",
      "is_correct": false
    }
  ]
}
```

**Parâmetros:**
| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| `quiz_id` | integer | ✅ Sim | ID do quiz |
| `question_text` | string | ✅ Sim | Texto da pergunta |
| `options` | array | ✅ Sim | Lista de opções |
| `options[].question_id` | integer | ✅ Sim | ID da pergunta |
| `options[].option_text` | string | ✅ Sim | Texto da opção |
| `options[].is_correct` | boolean | ❌ Não | Se é a resposta correta (padrão: false) |

**Resposta Esperada (201 Created):**
```json
{
  "msg": "success"
}
```

**Possíveis Erros:**

| Status | Erro | Descrição |
|--------|------|-----------|
| 401 | Unauthorized | Token ausente ou inválido |
| 404 | Not Found | Quiz não existe |
| 403 | Forbidden | Apenas professores podem adicionar perguntas |

---

### 18. Responder Quiz

**Endpoint:** `POST /lessons/quiz/answer`

**Autenticação:** ✅ Requer (Token JWT)

**Query Parameters:**
| Parâmetro | Tipo | Obrigatório | Descrição |
|-----------|------|-------------|-----------|
| `lesson_id` | integer | ✅ Sim | ID da aula |
| `quiz_id` | integer | ✅ Sim | ID do quiz |
| `answer_option_ids` | array[integer] | ✅ Sim | IDs das opções selecionadas |

**Body:** Vazio (enviar `{}` ou sem body)

**Resposta Esperada (200 OK):**
```json
{
  "msg": "success"
}
```

**Possíveis Erros:**

| Status | Erro | Descrição |
|--------|------|-----------|
| 401 | Unauthorized | Token ausente ou inválido |
| 404 | Not Found | Quiz ou aula não existe |
| 400 | Bad Request | Aluno já respondeu este quiz |
| 422 | Unprocessable Entity | Resposta inválida |

**Exemplo com cURL:**
```bash
curl -X POST "http://localhost:8000/lessons/quiz/answer?lesson_id=2&quiz_id=1&answer_option_ids=2" \
  -H "Authorization: Bearer seu_token_aqui"
```

**Exemplo com JavaScript:**
```javascript
const token = localStorage.getItem('token');
const lessonId = 2;
const quizId = 1;
const selectedOptionIds = [2]; // IDs das opções selecionadas

const queryParams = new URLSearchParams({
  lesson_id: lessonId,
  quiz_id: quizId,
  answer_option_ids: selectedOptionIds.join(',')
});

const response = await fetch(`http://localhost:8000/lessons/quiz/answer?${queryParams}`, {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`
  }
});

const data = await response.json();
console.log(data);
```

---

## 🔑 Tratamento de Tokens JWT

### Como Armazenar o Token

**LocalStorage (não recomendado para produção, mas útil para desenvolvimento):**
```javascript
// Após login
const response = await fetch('http://localhost:8000/auth/login', {...});
const data = await response.json();
localStorage.setItem('token', data.access_token);

// Para usar em requisições posteriores
const token = localStorage.getItem('token');
```

**Exemplo de Interceptador (Axios):**
```javascript
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000'
});

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

export default api;
```

### Renovação de Tokens

Os tokens expiram em **30 minutos**. Quando expirar, será necessário fazer login novamente.

**Detecção de Token Expirado:**
```javascript
const response = await fetch('http://localhost:8000/courses/', {
  headers: {
    'Authorization': `Bearer ${token}`
  }
});

if (response.status === 401) {
  // Token expirou, fazer logout
  localStorage.removeItem('token');
  // Redirecionar para login
  window.location.href = '/login';
}
```

---

## ⚠️ Mensagens de Erro Comuns

| Status | Erro | Solução |
|--------|------|---------|
| 401 | Unauthorized | Adicione o token no header `Authorization: Bearer token` |
| 403 | Forbidden | Você não tem permissão para esta ação |
| 404 | Not Found | O recurso não existe, verifique o ID |
| 422 | Unprocessable Entity | Verifique o formato dos dados enviados |
| 500 | Internal Server Error | Erro no servidor, contate o desenvolvedor |

---

## 🧪 Ferramentas Úteis para Testes

### Swagger UI (Documentação Interativa)
```
http://localhost:8000/docs
```

### ReDoc (Documentação Alternativa)
```
http://localhost:8000/redoc
```

### Testar com Postman
1. Crie um novo request
2. Defina o método HTTP (GET, POST, etc)
3. Digite a URL do endpoint
4. Na aba "Headers", adicione:
   - `Content-Type: application/json`
   - `Authorization: Bearer seu_token_aqui`
5. Na aba "Body", adicione o JSON com os dados

---

## 📞 Suporte e Dúvidas

Se encontrar algum problema ou tiver dúvidas sobre os endpoints:

1. Verifique a documentação Swagger em `/docs`
2. Confira os exemplos de código neste documento
3. Verifique se o token está válido e não expirou
4. Contate o time de backend

---

**Última atualização:** 24 de Abril de 2026
