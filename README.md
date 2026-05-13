# 🎓 TrAI Questions (Plataforma de Avaliação Inteligente)

Uma plataforma educacional inovadora que automatiza a correção de questões discursivas utilizando Inteligência Artificial (Large Language Models). O sistema compara a resposta do aluno com uma "Rubrica Secreta" definida pelo professor e gera feedback instantâneo, estruturado e pedagógico.

## 🚀 Principais Funcionalidades

- **Correção Baseada em Rubricas:** A IA avalia as respostas estritamente com base nos critérios cadastrados pelo professor, minimizando alucinações e garantindo o rigor académico.
- **Feedback Multicritério:** Retorno detalhado categorizado em "Nota", "Pontos Fortes", "Pontos a Melhorar" e "Comentário do Professor".
- **Integração LLM Resiliente:** Comunicação direta com a API da OpenAI (ChatGPT), com tratamento de erros (HTTP 503) para indisponibilidade de rede ou falhas na API.
- **Painel Administrativo:** Gestão completa de questões, submissões e rubricas através do Django Admin.

## 🛠️ Tecnologias Utilizadas

**Frontend:**
- [React 18](https://reactjs.org/) (com Vite)
- JavaScript / JSX
- Integração de API via Axios

**Backend:**
- [Python 3](https://www.python.org/)
- [Django 5](https://www.djangoproject.com/) & Django REST Framework
- SQLite (Base de dados padrão)
- Python-dotenv (Gestão de variáveis de ambiente)

**Inteligência Artificial:**
- OpenAI API (`gpt-3.5-turbo` / `gpt-4o`)
- Engenharia de Prompts com *Direct Context Injection* e *Format Forcing* (retorno estrito em JSON).

## ⚙️ Arquitetura e Fluxo de Dados

1. **Entrada:** O aluno envia a sua resposta dissertativa através do Frontend (React).
2. **Processamento:** O Backend (Django) recebe o pedido, procura o enunciado e a rubrica correspondente na base de dados.
3. **Inferência:** O servidor monta um prompt dinâmico e aciona a API da OpenAI.
4. **Persistência:** A IA devolve um JSON estruturado. O sistema guarda a nota e o feedback na base de dados para manter o histórico.
5. **Apresentação:** O Frontend recebe os dados processados e exibe os cartões de avaliação para o aluno em tempo real.

## 💻 Como executar o projeto localmente

Siga as instruções abaixo para executar os dois ambientes (Backend e Frontend) na sua máquina.

### Pré-requisitos
- Python 3.x
- Node.js (v18+)

### Passo 1: Configurar o Backend (Django)

Abra um terminal e aceda à pasta `backend`:
```bash
cd backend
Crie um ambiente virtual e ative-o (opcional, mas recomendado):

Bash
python -m venv venv
# No Windows: venv\Scripts\activate
# No Mac/Linux: source venv/bin/activate
Instale as dependências necessárias:

Bash
pip install django djangorestframework django-cors-headers openai python-dotenv
Configuração da Chave de API:
Crie um ficheiro chamado .env na pasta backend (junto ao manage.py).
Nota: Por questões de segurança, este ficheiro está ignorado no GitHub e não é partilhado publicamente.
Insira a sua chave válida da OpenAI no ficheiro recém-criado:

Snippet de código
OPENAI_API_KEY="sk-SUA_CHAVE_AQUI"
Execute as migrações da base de dados e inicie o servidor:

Bash
python manage.py migrate
python manage.py createsuperuser # (Opcional) Para aceder ao painel de administração
python manage.py runserver
O backend estará a correr em http://localhost:8000
```

### Passo 2: Configurar o Frontend (React/Vite)
Abra um novo terminal (mantenha o backend a correr em segundo plano) e aceda à pasta `frontend`:
```
Bash
cd frontend
Instale as dependências do Node:

Bash
npm install
Inicie o servidor de desenvolvimento:

Bash
npm run dev
O frontend estará acessível em http://localhost:5173
```

🔒 Segurança e Boas Práticas

* Proteção de Credenciais: As chaves de API nunca são expostas ao cliente ou publicadas no repositório (protegidas via ficheiro .env).

* Resiliência: Tratamento de exceções implementado no servidor para evitar quebras totais da aplicação devido a falhas de serviços de terceiros.

Desenvolvido como Projeto Integrador.
