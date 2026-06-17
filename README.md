# 🚀 Developer Intelligence Platform

An AI-powered developer assistant capable of semantic repository understanding using Retrieval-Augmented Generation (RAG), vector embeddings, and LLM-powered repository chat.

---

## ✨ Features

- 🔍 Semantic Repository Search
- 💬 AI-Powered Repository Chat
- 🧠 RAG Pipeline
- 📦 GitHub Repository Parsing
- ⚡ Streaming AI Responses
- 🗂️ Multi-Repository Isolation
- 🧩 Intelligent Code Chunking
- 📚 ChromaDB Vector Storage

---
# System Architecture & Diagrams

---

## 🧠 Repository Ingestion Pipeline

```mermaid
flowchart TD
    Start(["👤 User Submits<br/>GitHub Repo URL"]) --> Clone["GitPython<br/>Clone Repository"]

    Clone --> Parse["Repository Parsing<br/>(walk file tree, filter by extension)"]

    Parse --> Chunk["Code Chunking<br/>(fixed-size token/line chunks,<br/>with overlap between chunks)"]

    Chunk --> Embed["Sentence Transformers<br/>Generate Embeddings"]

    Embed --> CollectionCheck{"Collection Exists<br/>for This Repo?"}
    CollectionCheck -- "No" --> CreateCollection["Create New Named<br/>ChromaDB Collection<br/>(e.g. repo_&lt;name&gt;_&lt;hash&gt;)"]
    CollectionCheck -- "Yes" --> UseExisting["Use Existing Collection"]

    CreateCollection --> Store["Store Chunks + Embeddings<br/>+ Metadata (file path, line range)"]
    UseExisting --> Store

    Store --> Ready(["✅ Repository Ready<br/>for Semantic Chat"])

    style Clone fill:#1a1a1a,color:#fff,stroke:#fff
    style Chunk fill:#374151,color:#fff,stroke:#fff
    style CreateCollection fill:#b91c1c,color:#fff,stroke:#fff
    style Ready fill:#1a1a1a,color:#fff,stroke:#fff
```

---

## 💬 Repository Chat Sequence (RAG Retrieval + Streaming)

```mermaid
sequenceDiagram
    actor User
    participant UI as Streamlit Chat UI
    participant App as app.py
    participant ST as Sentence Transformers
    participant Chroma as ChromaDB<br/>(Repo's Collection)
    participant LC as LangChain
    participant Groq as Groq API

    User->>UI: Ask question about repo
    UI->>App: Query + active repo_id

    App->>ST: Embed user query
    ST-->>App: Query embedding

    App->>Chroma: Similarity search<br/>(scoped to this repo's collection)
    Chroma-->>App: Top-K relevant chunks<br/>(code + file path + line range)

    App->>LC: Build prompt<br/>(query + retrieved chunks as context)
    LC->>Groq: Send prompt (streaming=true)

    loop Token Stream
        Groq-->>LC: Next token chunk
        LC-->>App: Forward chunk
        App-->>UI: Render incrementally
        UI-->>User: Text appears progressively
    end

    Groq-->>LC: Stream complete
    LC-->>App: Final response (+ cited sources)
    App-->>UI: Render source references
    UI-->>User: Show file/line citations<br/>below response
```

---

## 🗂️ Multi-Repository Isolation

```mermaid
graph TB
    subgraph App["Developer Intelligence Platform"]
        direction TB
        Session["Active Session<br/>(one repo selected at a time)"]
    end

    subgraph ChromaInstance["ChromaDB Instance"]
        direction LR
        Coll1[("Collection:<br/>repo_alpha_a1b2")]
        Coll2[("Collection:<br/>repo_beta_c3d4")]
        Coll3[("Collection:<br/>repo_gamma_e5f6")]
    end

    Repo1["GitHub: project-alpha"] -->|"Clone + Ingest"| Coll1
    Repo2["GitHub: project-beta"] -->|"Clone + Ingest"| Coll2
    Repo3["GitHub: project-gamma"] -->|"Clone + Ingest"| Coll3

    Session -->|"Queries ONLY<br/>the selected repo's collection"| Coll1
    Session -.->|"No cross-collection access"| Coll2
    Session -.->|"No cross-collection access"| Coll3

    style Coll1 fill:#b91c1c,color:#fff,stroke:#fff
    style Coll2 fill:#374151,color:#fff,stroke:#fff
    style Coll3 fill:#374151,color:#fff,stroke:#fff
    style Session fill:#1a1a1a,color:#fff,stroke:#fff
```




## 🛠️ Tech Stack

### Frontend
- Streamlit

### AI / Backend
- Groq API
- Sentence Transformers
- ChromaDB
- LangChain

### Utilities
- GitPython
- Python Dotenv

---

## ⚙️ Installation

### Clone Repository

```bash
git clone <your_repo_url>
cd developer-intelligence-platform
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

#### Windows

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Setup Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_api_key_here
```

### Run Application

```bash
streamlit run app.py
```
---

## 🚀 Future Improvements

- PR Review AI
- Bug Fix Assistant
- Documentation Generator
- GitHub OAuth
- Multi-Agent Workflows

---

## 👨‍💻 Author

Rudra Raj
