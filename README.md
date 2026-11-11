# 🚀 Analisador Inteligente de Feedback de Clientes

![Python](https://img.shields.io/badge/Python_3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI_API-412991?style=for-the-badge&logo=openai&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

Ferramenta em Python para **análise automatizada de sentimento, categorização e priorização de feedbacks de clientes** utilizando Modelos de Linguagem (LLMs) via API da OpenAI.

---

## 🎯 Funcionalidades

- **Classificação de Sentimento:** Identifica automaticamente se o feedback é `Positivo`, `Negativo` ou `Neutro`.
- **Categorização Inteligente:** Classifica cada relato em `Atendimento`, `Produto`, `Entrega`, `Preço` ou `Outro`.
- **Definição de Prioridade:** Atribui urgência (`Alta`, `Média` ou `Baixa`) para triagem rápida de suporte.
- **Resumo Executivo:** Gera uma síntese de até 100 caracteres destacando o ponto central do elogio ou problema.
- **Relatórios e Exportação:** Consolida métricas estatísticas no terminal e exporta os resultados estruturados em JSON.

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.8+**
- **OpenAI Python SDK** (`gpt-3.5-turbo` com saída estruturada em JSON)
- **JSON & Datetime** para persistência e rastreabilidade temporal

---

## 📦 Como Executar

1. **Clone o repositório e instale as dependências:**
   ```bash
   git clone https://github.com/zlluska/analisador-feedback-clientes.git
   cd analisador-feedback-clientes
   pip install -r requirements.txt
   ```

2. **Configure sua chave da API OpenAI:**
   - **Linux / macOS:**
     ```bash
     export OPENAI_API_KEY="sua-chave-aqui"
     ```
   - **Windows (PowerShell):**
     ```powershell
     $env:OPENAI_API_KEY="sua-chave-aqui"
     ```

3. **Execute o analisador:**
   ```bash
   python feedback_analyzer.py
   ```

---

## 📊 Exemplo de Saída

```json
{
  "id": 1,
  "author": "Maria Silva",
  "source": "whatsapp",
  "sentimento": "Negativo",
  "categoria": "Entrega",
  "prioridade": "Alta",
  "resumo": "Atraso de 5 dias na entrega do pedido e falta de atualização no rastreio."
}
```

---

## ⚠️ Limitações Conhecidas & Próximos Passos

- **Processamento Sequencial (Síncrono):** Atualmente analisa os feedbacks item a item via chamada HTTP síncrona; para lotes de milhares de mensagens, o próximo passo é migrar para `AsyncOpenAI` (`asyncio`) ou Batch API.
- **Armazenamento em Arquivo Local:** Os relatórios são exportados em JSON no disco local; planeja-se integração opcional com **SQLite / PostgreSQL** e dashboard em **Streamlit**.

---

## 📝 Licença

Distribuído sob a licença **MIT**. Veja [`LICENSE`](./LICENSE) para mais detalhes.

## 👤 Autor

**Lucas Fraga** — [GitHub (@zlluska)](https://github.com/zlluska)
