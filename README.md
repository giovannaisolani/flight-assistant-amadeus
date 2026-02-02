## :airplane: Flight Assistant

Assistente de linha de comando para buscar voos usando Amadeus + LangChain + OpenAI.

### 1️⃣ Pré-requisitos
python >= 3.10

Requisitos:

• conta na OpenAI
• conta no Amadeus
• conta no LangSmith (opcional)

Links:

https://platform.openai.com

https://developers.amadeus.com

https://smith.langchain.com

### 2️⃣ Criar chaves de API

OpenAI
export OPENAI_API_KEY="sk-..."

Amadeus
export AMADEUS_CLIENT_ID="..."
export AMADEUS_CLIENT_SECRET="..."

LangSmith (opcional)
export LANGSMITH_API_KEY="..."
export LANGSMITH_TRACING=true
export LANGSMITH_PROJECT=flight-assistant


No Windows:

setx OPENAI_API_KEY "sk-..."


No Colab:

import os
os.environ["OPENAI_API_KEY"] = "..."

### 3️⃣ Instalar dependências
pip install -r requirements.txt


### 4️⃣ Rodar o projeto
python main.py

### 5️⃣ Exemplo de uso
✈️ Flight Assistant

F.A.:Para onde você quer viajar?

User: Quero voar para roma, partindo de sao paulo por volta do dia 20/07/2026, para ficar 
por 10 dias, apenas voos com no máximo uma conexão que incluam bagagem

Buscando...


Resultado:

Opção 1 - mais barata
- Preço total: BRL 5.035,63
- Itinerário de ida (GRU → FCO):
  - GRU (07/07, 21:45) → AMS (07/08, 14:20) via KL (operado pela KLM), 1 conexão em AMS
  - AMS (07/08, 16:35) → FCO (07/08, 18:45), direto
- Itinerário de volta (FCO → GRU):
  - FCO (07/27, 06:30) → AMS (07/27, 08:50), direto
  - AMS (07/27, 12:55) → GRU (07/27, 19:50), direto
- Companhia/voos: KL via código G3 (KLM)
- Bagagem: 1 mala de cabine incluída; bagagem despachada incluída nesta tarifa LIGHT
- Duração aproximada: ida ~16h total; volta ~18h20m total
...

### Estrutura do repo

```text
flight-assistant-amadeus/
├── main.py
├── agent.py
├── tools/
│   ├── flights.py
│   └── aggregate.py
├── requirements.txt
└── README.md
```