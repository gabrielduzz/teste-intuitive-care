# Teste Técnico - Intuitive Care

Aplicação Full Stack desenvolvida para monitoramento, análise e visualização de despesas de operadoras de planos de saúde, utilizando dados abertos da ANS.

![Dashboard Preview](screenshots/home.png)

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

### 🐧 No Linux/Mac
```bash
chmod +x run.sh
./run.sh   
```
**O que esse script faz?**
Ele automatiza o setup para você não perder tempo:

1.  Limpa volumes antigos do Docker (pra garantir que não tenha lixo de execuções anteriores).
    
2.  Sobe o container do PostgreSQL.
    
3.  Roda o pipeline completo de ETL (scraping -> processamento -> importação pro banco).
    
4.  Te avisa quando terminar.
    

### 🐍 Preparando o Backend

Em um terminal separado:

```bash
# Suba o servidor
uvicorn backend.main:app --reload
```

*   **API:** http://localhost:8000
    
*   **Docs (Swagger):** http://localhost:8000/docs
    

### 🎨 Iniciando o Frontend

Em outro terminal:
```bash
cd frontend
npm install
npm run dev
```

*   **Dashboard:** http://localhost:5173
    

### ⚠️ Nota sobre os Dados (Backup de Segurança)

O script tenta baixar os dados direto do site da ANS em tempo real. Mas a gente sabe que sites do governo às vezes ficam instáveis ou lentos.

**Plano B:** Já deixei os arquivos .csv processados e prontos na pasta data/processed.Se o script de scraping falhar por conexão, o sistema é inteligente o suficiente para usar esses arquivos locais. Assim você consegue testar a aplicação sem ficar travado esperando download.

⚖️ Trade-offs e Decisões Técnicas
---------------------------------

Durante o desenvolvimento, precisei tomar algumas decisões de arquitetura. Abaixo explico o porquê de cada escolha, focando no contexto do teste e boas práticas.

### 1\. Processamento de Dados (ETL)

**Decisão:** Processamento em Memória (Pandas).

*   **Por que?** O volume de dados trimestral da ANS, embora pareça grande em linhas, cabe tranquilamente na memória RAM de máquinas modernas. Usar Pandas permitiu escrever um código muito mais limpo e rápido de implementar do que criar um processamento incremental ou em stream, que seria "overengineering" para esse cenário.
    

### 2\. Tratamento de Dados Inválidos

**Decisão:** Limpeza e Padronização.

*   **Por que?** Em vez de descartar qualquer linha com erro, optei por tentar salvar o dado. Para CNPJs, removi caracteres não numéricos e garanti o _padding_ com zeros à esquerda. Se mesmo assim o dado for inválido, ele é mantido para fins de auditoria, mas não entra nas métricas financeiras críticas.
    

### 3\. Banco de Dados: Normalização

**Decisão:** Tabelas Normalizadas (dim\_companies e fact\_expenses).

*   **Por que?** Poderia ter feito uma tabela única (plana), mas optei por separar. A dimensão de empresas (dim\_companies) evita que a gente repita a Razão Social e UF milhões de vezes na tabela de despesas, economizando espaço e facilitando a atualização cadastral se a empresa mudar de nome.
    

### 4\. Banco de Dados: Tipos Numéricos

**Decisão:** DECIMAL/NUMERIC ao invés de FLOAT.

*   **Por que?** Regra de ouro em sistemas financeiros: nunca use Float para dinheiro por causa de erros de arredondamento de ponto flutuante. Usei DECIMAL para garantir precisão exata nos centavos.
    

### 5\. Backend: Framework

**Decisão:** FastAPI.

*   **Por que?** É mais performático que o Flask (assíncrono nativo) e a melhor parte: ele já me dá a documentação Swagger de graça e valida os dados de entrada/saída com o Pydantic. Isso poupou muito tempo de validação manual de JSON.
    

### 6\. Estratégia de Paginação

**Decisão:** Offset-based (LIMIT/OFFSET).

*   **Por que?** Num dashboard administrativo, o usuário quer saber "quantas páginas tem" e poder pular da página 1 para a 10. Paginação por cursor (como em redes sociais) é mais rápida para volumes gigantes, mas ruim para navegação e tabelas clássicas. Com os índices que criei no banco, o Offset funciona super bem aqui.
    

### 7\. Frontend: Busca

**Decisão:** Busca no Servidor (Server-side).

*   **Por que?** Carregar todas as operadoras no navegador do cliente pesaria demais a página inicial. Fazendo a busca no servidor (usando ILIKE no SQL), transferimos o peso do processamento para o banco, que é feito pra isso, deixando o front leve e rápido.
    

### 8\. Frontend: Estado

**Decisão:** Composition API & Refs (Simples).

*   **Por que?** Não usei Pinia ou Vuex porque não precisava. O estado da aplicação é local (apenas a lista da tela atual ou os detalhes da empresa). Usar uma lib de gerenciamento de estado global só adicionaria complexidade desnecessária (boilerplate) sem ganho real. Mantive o princípio KISS (_Keep It Simple, Stupid_).
    

🌟 Diferenciais
---------------

Além do básico funcional, implementei alguns pontos extras para garantir qualidade:

*   **Arquitetura Limpa:** O Backend não é um "arquivo linguiça". Separei rotas, models e conexão com banco. O Frontend também está componentizado.
    
*   **Performance:**
    
    *   No Frontend, uso Promise.all para disparar requisições em paralelo (dados da empresa + despesas), carregando a tela de detalhes na metade do tempo.
        
    *   No Banco, criei índices específicos para as colunas que a gente mais busca (CNPJ e Datas).
        
*   **UX/UI:** O layout é responsivo, tem feedback visual de "Carregando..." e trata erros de forma amigável, sem estourar código na cara do usuário.
    
*   **Resiliência:** O script de ETL tem try/except robusto. Se um arquivo falhar, ele avisa e tenta continuar o resto, em vez de quebrar o processo todo.
    

## 📂 Estrutura do Projeto

```text
teste-intuitive-care/
├── 📂 backend/            # API RESTful (FastAPI + SQLAlchemy)
├── 📂 frontend/           # Dashboard Interativo (Vue.js 3 + TypeScript)
├── 📂 data/               # Armazenamento de dados (Raw & Processed)
├── 📂 src/                # Scripts do Pipeline ETL (Scraping, Validação, Agregação)
├── 🐳 docker-compose.yml  # Orquestração do Banco de Dados (PostgreSQL)
└── 🚀 run.bat / run.sh    # Scripts de Automação ("One-click setup")
```

📬 Postman
----------

Deixei um arquivo collection.json na raiz. É só importar no Postman que todas as rotas já estão configuradas para teste.
