# Teste Técnico - Intuitive Care

Aplicação Full Stack desenvolvida para monitoramento, análise e visualização de despesas de operadoras de planos de saúde, utilizando dados abertos da ANS.

![Dashboard Preview](screenshots/dashboard.png)
*(Certifique-se de que a imagem screenshots/dashboard.png existe no projeto)*

## 📋 Sobre o Projeto

Este projeto consiste em uma solução ponta-a-ponta (End-to-End) que realiza:
1.  **ETL Automatizado:** Scraping, limpeza, transformação e validação de dados da ANS.
2.  **API RESTful:** Backend performático para servir dados paginados e estatísticas.
3.  **Dashboard Interativo:** Frontend moderno para visualização de indicadores e histórico financeiro.

---

## 🚀 Como Executar

O projeto foi desenhado para ser executado de forma simples, mas permite controle granular se necessário.

### Pré-requisitos
- **Docker & Docker Compose** (Essencial para o Banco de Dados)
- **Python 3.10+**
- **Node.js 18+**


# Crie e ative o ambiente virtual
```bash
python -m venv venv
# Windows: venv\Scripts\activate
# Linux/Mac: source venv/bin/activate
```

### Execução Automática ⚡

Criei scripts de automação que configuram o ambiente, sobem o banco, instalam dependências e rodam o pipeline de dados completo.

**No Windows:**
```bash
./run.bat
```

No Linux/Mac:

```bash
chmod +x run.sh
./run.sh
```
O script irá:

Limpar volumes antigos do Docker (para evitar duplicação).

Subir o PostgreSQL.

Executar o Pipeline ETL (scraping -> processing -> db import).

Exibir os comandos finais para rodar o servidor e o frontend.

Prepare o ambiente Python:

```bash
uvicorn backend.main:app --reload
```
A API estará disponível em: http://localhost:8000 Documentação Swagger: http://localhost:8000/docs

3. Frontend
Em um novo terminal, inicie a interface:

```bash
cd frontend
npm install
npm run dev
```
O Dashboard estará disponível em: http://localhost:5173

⚠️ Nota sobre os Dados (Backup)
O pipeline de dados conecta-se em tempo real ao site da ANS. Como serviços governamentais podem apresentar instabilidade:

Backup Incluído: O projeto já contém os arquivos .csv processados na pasta data/processed.

Contingência: Se o script de scraping falhar, o sistema é capaz de prosseguir a importação utilizando esses arquivos locais, garantindo que o avaliador consiga testar a aplicação sem bloqueios.

⚖️ Trade-offs e Decisões Técnicas
Conforme solicitado, abaixo justifico as decisões arquiteturais tomadas durante o desenvolvimento.

1. Backend: Framework
Escolha: FastAPI (Opção B)

Justificativa: Em comparação ao Flask, o FastAPI oferece performance superior (ASGI) e validação de dados nativa via Pydantic. A geração automática da documentação (Swagger UI) acelera o desenvolvimento e facilita a auditoria da API, reduzindo a necessidade de escrever documentação manual para cada rota.

2. Banco de Dados: Estratégia de Paginação
Escolha: Offset-based (Opção A)

Justificativa: O requisito de negócio (Dashboard) implica que o usuário pode querer navegar para páginas específicas ou ver o total de registros. A paginação baseada em cursor (Cursor-based) é excelente para scroll infinito, mas dificulta o "salto" de páginas. Com índices adequados no banco, o Offset atende perfeitamente ao volume de dados proposto.

3. API: Cache vs Real-time
Escolha: Queries Diretas Otimizadas (Opção A)

Justificativa: A periodicidade de atualização dos dados da ANS é trimestral. Implementar cache (como Redis) adicionaria complexidade de infraestrutura para dados que são essencialmente estáticos. A otimização foi feita no nível do banco de dados, criando índices compostos (CREATE INDEX) para garantir respostas em milissegundos.

4. Frontend: Busca e Filtragem
Escolha: Busca no Servidor (Opção A)

Justificativa: Embora o dataset de teste seja pequeno, uma aplicação real de operadoras conteria milhares de registros. Carregar tudo no cliente (Client-side) prejudicaria o "Time to Interactive" e o consumo de memória do navegador. A busca no servidor (Server-side search) com filtros SQL ILIKE é a solução escalável.

5. Frontend: Gerenciamento de Estado
Escolha: Composition API & Refs (Opção C)

Justificativa: A aplicação possui escopo bem definido e não apresenta complexidade de compartilhamento de estado global profundo que justificasse o uso de Pinia ou Vuex. O uso de refs e composables nativos do Vue 3 mantém o código mais limpo (KISS - Keep It Simple, Stupid) e facilita a manutenção.

🌟 Diferenciais Implementados
Além dos requisitos obrigatórios, o projeto conta com:

Arquitetura Limpa: Separação clara de responsabilidades. Backend organizado em camadas (Router, Controller, Service, Model) e Frontend componentizado.

Performance:

Uso de Promise.all no frontend para carregamento paralelo de dados.

Índices no PostgreSQL para otimizar queries de agregação.

UX/UI Polida:

Interface moderna e responsiva.

Tratamento de erros amigável (Feedback visual ao usuário).

Formatação inteligente de valores monetários e datas.

Resiliência: O script de ETL possui tratamento de falhas (try/except) e fallback para arquivos locais.

📂 Estrutura do Projeto
Plaintext
teste-intuitive-care/
├── backend/            # API FastAPI
│ 
├── frontend/           # Aplicação Vue.js

├── data/               # Arquivos CSV/ZIP 
├── sql/                # Queries SQL
├── src/                # Scripts de ETL 
├── run.bat / run.sh    # Scripts de Automação
└── docker-compose.yml  # Infraestrutura

📬 Coleção Postman
O arquivo collection.json na raiz do projeto contém a coleção completa para testes da API.
