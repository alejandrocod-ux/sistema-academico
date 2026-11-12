# Sistema Acadêmico — Trabalho Victor

API desenvolvida com FastAPI, SQLAlchemy e SQLite.

## Executar localmente

1. Crie e ative um ambiente virtual:
   ```bash
   python -m venv venv
   # Windows:
   venv\\Scripts\\activate
   ```
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. Copie `.env.example` para `.env` e defina `JWT_SECRET_KEY` com uma chave aleatória forte.
   O ZIP de trabalho também inclui um `.env` local para facilitar o primeiro teste; **não publique esse arquivo no GitHub**.
4. Inicie a API na pasta do projeto:
   ```bash
   uvicorn app.main:app --reload
   ```
5. Abra `http://127.0.0.1:8000/docs`.

## Autenticação

- `POST /auth/register`: cadastra usuário. A senha é armazenada com hash Argon2.
- `POST /auth/login`: recebe `email` e `senha`, retorna JWT com expiração.
- `GET /auth/me`: retorna os dados do usuário autenticado.
- `GET /alunos/` e `GET /professores/`: exigem `Authorization: Bearer <token>`.

No Swagger, faça o cadastro, copie o `access_token` retornado pelo login, clique em **Authorize**, cole somente o valor de `access_token` no campo **HTTPBearer** (o Swagger adiciona o prefixo `Bearer`) e teste as rotas protegidas.

## Observação sobre a Primeira Unidade

Os endpoints e arquivos dos CRUDs foram preservados. Nesta versão, as listagens de alunos e professores passaram a exigir autenticação; os demais endpoints CRUD continuam como estavam.

## Checklist de evidências para a entrega

1. Abra `/docs` e mostre os três endpoints da tag **Autenticação**.
2. Faça `POST /auth/register` com nome, e-mail e senha de pelo menos 8 caracteres.
3. Faça `POST /auth/login` com o mesmo e-mail e senha; copie `access_token`.
4. Use **Authorize** no Swagger e informe `Bearer <access_token>`.
5. Execute `GET /auth/me`, `GET /alunos/` e `GET /professores/`: devem responder 200.
6. Remova a autorização ou use um token inválido: as duas listagens protegidas devem responder 401.

**Segurança:** nunca envie o `.env` ao GitHub. O `.env.example` é o modelo seguro para compartilhar.
