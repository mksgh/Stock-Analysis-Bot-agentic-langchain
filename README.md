# 📈 Stock Market Analysis Bot - Agentic LangChain

A modular, agentic chatbot platform for stock market research and document retrieval, built with FastAPI, Streamlit, LangChain, Pinecone, and various LLM/embedding providers.

---

## Features

- **Document Ingestion:** Upload PDFs/DOCX files to build a vector knowledge base using Pinecone.
- **Conversational Agent:** Query the chatbot for stock market insights, document retrieval, and financial data.
- **Multi-Tool Integration:** Supports Bing, Tavily, Polygon, and more via LangChain tools.
- **LLM Flexibility:** Easily switch between Google, Groq, and other LLM providers.
- **Modern UI:** Streamlit-based frontend for chat and file upload.
- **Robust API:** FastAPI backend for ingestion and chat endpoints.
- **Customizable Configuration:** Easily adjust model, retriever, and tool settings via YAML config.
- **Extensible:** Add new tools, models, or data sources with minimal code changes.

---

## Project Structure

```
.
├── agents/
│   └── workflow.py
├── agent_tools/
│   └── tools.py
├── config/
│   └── config.yaml
├── data_ingestion/
│   └── ingestion.py
├── data_models/
│   └── models.py
├── exception/
│   └── exceptions.py
├── logger/
│   └── custom_logger.py
├── utils/
│   ├── config_loader.py
│   └── model_loader.py
├── main.py           # FastAPI backend
├── streamlit.py      # Streamlit frontend
├── .env              # Environment variables
├── requirements.txt
└── research/
    └── research.ipynb
```

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/TradingBot-agentic-langchain.git
cd TradingBot-agentic-langchain
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables

Create a `.env` file in the project root with your API keys:

```
GOOGLE_API_KEY=your_google_api_key
PINECONE_API_KEY=your_pinecone_api_key
GROQ_API_KEY=your_groq_api_key
POLYGON_API_KEY=your_polygon_api_key
TAVILY_API_KEY=your_tavily_api_key
AZURE_OPENAI_API_KEY=your_azure_openai_api_key
AZURE_OPENAI_ENDPOINT=your_azure_openai_endpoint
```

### 4. Configure the Application

Edit `config/config.yaml` to adjust model names, retriever settings, and tool parameters as needed.

### 5. Start the Backend (FastAPI)

```bash
uvicorn main:app --reload
```

### 6. Start the Frontend (Streamlit)

```bash
streamlit run streamlit.py
```

---

## Usage

- **Upload Documents:** Use the sidebar in the Streamlit app to upload PDF/DOCX files.
- **Chat:** Ask questions about the stock market or your uploaded documents in the chat interface.
- **API Endpoints:**
  - `POST /upload` — Upload and ingest files.
  - `POST /query` — Query the chatbot with a question.

---

## Configuration

Edit `config/config.yaml` to adjust:
- Model provider and names (Google, Azure, Groq)
- Retriever settings (`top_k`, `score_threshold`)
- Tool parameters (e.g., Tavily max results, Pinecone index name)

---

## Contributing

Pull requests and issues are welcome! Please open an issue to discuss your ideas or report bugs.

---

## License

MIT License

---

## Acknowledgements

- [LangChain](https://github.com/langchain-ai/langchain)
- [Pinecone](https://www.pinecone.io/)
- [Streamlit](https://streamlit.io/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [OpenAI](https://openai.com/)
- [Google Generative AI](https://ai.google/discover/generative-ai/)
- [Groq](https://groq.com/)
