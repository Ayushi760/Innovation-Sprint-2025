# 🧠 AI Knowledge Assistant - RAG Chatbot

A production-ready Retrieval-Augmented Generation (RAG) chatbot powered by Azure OpenAI that enables intelligent document querying and conversational AI interactions.

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.45.1-red.svg)](https://streamlit.io)
[![Azure OpenAI](https://img.shields.io/badge/Azure-OpenAI-green.svg)](https://azure.microsoft.com/en-us/products/ai-services/openai-service)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-1.0.12-orange.svg)](https://www.trychroma.com/)

## 🚀 Features

### Core Capabilities
- **🔍 Intelligent Document Search**: Semantic search across uploaded documents using vector embeddings
- **💬 Conversational AI**: Context-aware conversations with memory across sessions
- **📚 Multi-Format Support**: Process PDF, DOCX, and TXT documents
- **🎯 Source Attribution**: Get answers with referenced document sources
- **🧠 Context Memory**: Maintains conversation history for coherent interactions
- **⚡ Real-time Processing**: Fast document ingestion and query responses

### Interface Options
- **🖥️ Streamlit Web App**: Beautiful, interactive web interface
- **⌨️ Command Line Interface**: Full-featured CLI for power users
- **🔧 Modular Architecture**: Easy to integrate into existing applications

### Advanced Features
- **📊 Knowledge Base Management**: Add, search, and manage document collections
- **🔄 Session Management**: Multiple conversation sessions with independent contexts
- **🎨 Rich UI Components**: Progress indicators, metrics, and interactive elements
- **🛡️ Error Handling**: Robust error handling and user feedback
- **📈 Analytics**: Session statistics and knowledge base metrics

## 📋 Table of Contents

- [Installation](#-installation)
- [Configuration](#-configuration)
- [Quick Start](#-quick-start)
- [Usage](#-usage)
- [API Reference](#-api-reference)
- [Architecture](#-architecture)
- [Development](#-development)
- [Deployment](#-deployment)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

## 🛠️ Installation

### Prerequisites

- **Python 3.8+** (recommended: Python 3.9 or 3.10)
- **Azure OpenAI Service** account with API access
- **Git** for cloning the repository

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd rag_chatbot
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Verify Installation

```bash
python -c "import streamlit, chromadb, openai; print('✅ All dependencies installed successfully!')"
```

## ⚙️ Configuration

### Environment Setup

1. **Copy the example environment file:**
   ```bash
   cp .env.example .env
   ```

2. **Edit the `.env` file with your Azure OpenAI credentials:**
   ```env
   AZURE_OPENAI_API_KEY=your_azure_openai_api_key_here
   AZURE_OPENAI_ENDPOINT=your_azure_openai_endpoint_here
   AZURE_OPENAI_API_VERSION=2024-02-01
   AZURE_OPENAI_DEPLOYMENT_NAME=your_deployment_name_here
   AZURE_OPENAI_MODEL_NAME=gpt-4
   ```

### Azure OpenAI Setup

1. **Create an Azure OpenAI resource** in the Azure portal
2. **Deploy a model** (recommended: GPT-4 or GPT-3.5-turbo)
3. **Get your credentials** from the Azure portal:
   - API Key
   - Endpoint URL
   - Deployment name

### Configuration Validation

Run the configuration check:
```bash
python -c "from src.azure_openai_client import AzureOpenAIClient; client = AzureOpenAIClient(); print('✅ Configuration valid!' if client.test_connection() else '❌ Configuration invalid')"
```

## 🚀 Quick Start

### Option 1: Streamlit Web Interface (Recommended)

1. **Start the web application:**
   ```bash
   streamlit run streamlit_app.py
   ```

2. **Open your browser** to `http://localhost:8501`

3. **Initialize the assistant** using the sidebar Setup tab

4. **Upload documents** via the Knowledge tab

5. **Start chatting** with your documents!

### Option 2: Command Line Interface

1. **Start the CLI application:**
   ```bash
   python cli_app.py
   ```

2. **Add documents to knowledge base:**
   ```
   /add /path/to/your/documents
   ```

3. **Start asking questions:**
   ```
   You: What is the main topic of the uploaded documents?
   ```

## 📖 Usage

### Web Interface Guide

#### 1. Initial Setup
- Navigate to the **Setup** tab in the sidebar
- Verify your configuration status
- Click **"Start AI Assistant"** to initialize

#### 2. Document Management
- Go to the **Knowledge** tab
- Upload PDF, DOCX, or TXT files
- Click **"Add to Knowledge Base"** to process documents
- Monitor document count and status

#### 3. Conversation
- Use the main chat interface to ask questions
- View source references by expanding the **"View Sources"** section
- Manage sessions using the **Session** tab

#### 4. Session Management
- Create new sessions for different topics
- Clear chat history when needed
- View conversation statistics

### CLI Commands Reference

| Command | Description | Example |
|---------|-------------|---------|
| `/help` | Show available commands | `/help` |
| `/add <path>` | Add documents from folder | `/add ./documents` |
| `/info` | Show knowledge base info | `/info` |
| `/search <query>` | Search without generating response | `/search "machine learning"` |
| `/clear` | Clear conversation history | `/clear` |
| `/new` | Start new conversation session | `/new` |
| `/history` | Show conversation history | `/history` |
| `/quit` or `/exit` | Exit the application | `/quit` |

### Document Processing

#### Supported Formats
- **PDF**: Text extraction from PDF documents
- **DOCX**: Microsoft Word documents
- **TXT**: Plain text files

#### Processing Pipeline
1. **Document Reading**: Extract text from various formats
2. **Text Chunking**: Split documents into manageable chunks (500 characters)
3. **Embedding Generation**: Create vector embeddings using sentence transformers
4. **Vector Storage**: Store embeddings in ChromaDB for fast retrieval

#### Best Practices
- **File Organization**: Keep related documents in the same folder
- **File Naming**: Use descriptive filenames for better source attribution
- **Document Quality**: Ensure documents are text-readable (not scanned images)
- **Size Limits**: Individual files should be under 50MB for optimal performance

## 🔧 API Reference

### RAGChatbot Class

```python
from src.rag_chatbot import RAGChatbot

# Initialize chatbot
chatbot = RAGChatbot(persist_directory="chroma_db")

# Create session
session_id = chatbot.create_session()

# Add documents
chatbot.add_documents("./documents")

# Query with context
response, sources = chatbot.query("Your question here", session_id)

# Get knowledge base info
info = chatbot.get_knowledge_base_info()
```

### Key Methods

#### Document Management
```python
# Add documents from folder
chatbot.add_documents(folder_path: str)

# Get knowledge base information
info = chatbot.get_knowledge_base_info()

# Reset knowledge base
chatbot.reset_knowledge_base()

# Search documents
results = chatbot.search_documents(query: str, n_results: int = 5)
```

#### Session Management
```python
# Create new session
session_id = chatbot.create_session()

# Get conversation history
history = chatbot.get_conversation_history(session_id: str)

# Clear conversation
chatbot.clear_conversation(session_id: str)

# Get session info
info = chatbot.get_session_info(session_id: str)
```

#### Querying
```python
# Query with session context
response, sources = chatbot.query(
    question: str, 
    session_id: str, 
    n_chunks: int = 3
)

# Simple query without session
response, sources = chatbot.simple_query(
    question: str, 
    n_chunks: int = 3
)
```

## 🏗️ Architecture

### System Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Streamlit     │    │   CLI App       │    │   Your App      │
│   Interface     │    │   Interface     │    │   Integration   │
└─────────┬───────┘    └─────────┬───────┘    └─────────┬───────┘
          │                      │                      │
          └──────────────────────┼──────────────────────┘
                                 │
                    ┌─────────────▼───────────────┐
                    │      RAGChatbot Core        │
                    │   (Main Orchestrator)       │
                    └─────────────┬───────────────┘
                                  │
        ┌─────────────────────────┼─────────────────────────┐
        │                         │                         │
┌───────▼────────┐    ┌──────────▼──────────┐    ┌─────────▼─────────┐
│ Vector Database│    │ Azure OpenAI Client │    │Conversation Memory│
│   (ChromaDB)   │    │  (GPT-4/3.5-turbo) │    │  (Session Mgmt)   │
└────────────────┘    └─────────────────────┘    └───────────────────┘
        │
┌───────▼────────┐
│Document Processor│
│ (PDF/DOCX/TXT) │
└────────────────┘
```

### Component Details

#### 1. **RAGChatbot** (`src/rag_chatbot.py`)
- **Purpose**: Main orchestrator class
- **Responsibilities**: Coordinate between components, manage sessions, handle queries
- **Key Features**: Error handling, response generation, session management

#### 2. **VectorDatabase** (`src/vector_database.py`)
- **Purpose**: Vector storage and retrieval
- **Technology**: ChromaDB with sentence transformers
- **Features**: Semantic search, context extraction, collection management

#### 3. **AzureOpenAIClient** (`src/azure_openai_client.py`)
- **Purpose**: Interface with Azure OpenAI services
- **Features**: Response generation, query contextualization, connection testing
- **Models**: GPT-4, GPT-3.5-turbo support

#### 4. **ConversationMemory** (`src/conversation_memory.py`)
- **Purpose**: Manage conversation sessions and history
- **Features**: Multi-session support, history formatting, session analytics

#### 5. **DocumentProcessor** (`src/document_processor.py`)
- **Purpose**: Process and prepare documents for vector storage
- **Supported Formats**: PDF, DOCX, TXT
- **Features**: Text extraction, chunking, metadata handling

### Data Flow

1. **Document Ingestion**:
   ```
   Documents → Document Processor → Text Chunks → Vector Embeddings → ChromaDB
   ```

2. **Query Processing**:
   ```
   User Query → Context from Memory → Query Contextualization → Vector Search → 
   Context Retrieval → Response Generation → Memory Update → User Response
   ```

## 🔧 Development

### Project Structure

```
rag_chatbot/
├── src/                          # Core application modules
│   ├── __init__.py
│   ├── rag_chatbot.py           # Main RAG chatbot class
│   ├── azure_openai_client.py   # Azure OpenAI integration
│   ├── vector_database.py       # ChromaDB vector operations
│   ├── conversation_memory.py   # Session and memory management
│   └── document_processor.py    # Document processing utilities
├── streamlit_app.py             # Streamlit web interface
├── cli_app.py                   # Command-line interface
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment variables template
├── .gitignore                   # Git ignore rules
├── chroma_db/                   # ChromaDB persistence directory
├── temp_uploads/                # Temporary file storage
└── README.md                    # This file
```

### Development Setup

1. **Clone and setup development environment:**
   ```bash
   git clone <repository-url>
   cd rag_chatbot
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```

2. **Set up pre-commit hooks (optional):**
   ```bash
   pip install pre-commit
   pre-commit install
   ```

3. **Run tests:**
   ```bash
   python -m pytest tests/  # If tests are available
   ```

### Code Style and Standards

- **Python Style**: Follow PEP 8 guidelines
- **Type Hints**: Use type hints for better code documentation
- **Docstrings**: Document all public methods and classes
- **Error Handling**: Implement comprehensive error handling
- **Logging**: Use appropriate logging levels

### Adding New Features

#### 1. Adding New Document Types

```python
# In src/document_processor.py
def read_new_format_file(file_path: str) -> str:
    """Add support for new document format"""
    # Implementation here
    pass

# Update read_document function to include new format
```

#### 2. Adding New Vector Database Backends

```python
# Create new file: src/vector_database_new.py
class NewVectorDatabase:
    """Alternative vector database implementation"""
    # Implementation here
    pass
```

#### 3. Extending Conversation Memory

```python
# In src/conversation_memory.py
def add_advanced_memory_feature(self):
    """Add new memory management feature"""
    # Implementation here
    pass
```

## 🚀 Deployment

### Production Deployment Options

#### Option 1: Docker Deployment

1. **Create Dockerfile:**
   ```dockerfile
   FROM python:3.9-slim
   
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   
   COPY . .
   
   EXPOSE 8501
   CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
   ```

2. **Build and run:**
   ```bash
   docker build -t rag-chatbot .
   docker run -p 8501:8501 --env-file .env rag-chatbot
   ```

#### Option 2: Cloud Platform Deployment

**Streamlit Cloud:**
1. Push code to GitHub
2. Connect repository to Streamlit Cloud
3. Add environment variables in Streamlit Cloud settings
4. Deploy automatically

**Azure Container Instances:**
```bash
az container create \
  --resource-group myResourceGroup \
  --name rag-chatbot \
  --image your-registry/rag-chatbot:latest \
  --ports 8501 \
  --environment-variables AZURE_OPENAI_API_KEY=your-key
```

**AWS ECS/Fargate:**
- Use the provided Dockerfile
- Create ECS task definition
- Deploy to Fargate for serverless scaling

#### Option 3: Traditional Server Deployment

1. **Set up production server:**
   ```bash
   # Install dependencies
   sudo apt update
   sudo apt install python3 python3-pip nginx
   
   # Clone and setup application
   git clone <repository-url>
   cd rag_chatbot
   pip3 install -r requirements.txt
   ```

2. **Configure reverse proxy (Nginx):**
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       location / {
           proxy_pass http://localhost:8501;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

3. **Set up systemd service:**
   ```ini
   [Unit]
   Description=RAG Chatbot
   After=network.target
   
   [Service]
   Type=simple
   User=your-user
   WorkingDirectory=/path/to/rag_chatbot
   ExecStart=/usr/bin/python3 -m streamlit run streamlit_app.py
   Restart=always
   
   [Install]
   WantedBy=multi-user.target
   ```

### Production Configuration

#### Environment Variables
```env
# Production settings
AZURE_OPENAI_API_KEY=your_production_api_key
AZURE_OPENAI_ENDPOINT=your_production_endpoint
AZURE_OPENAI_API_VERSION=2024-02-01
AZURE_OPENAI_DEPLOYMENT_NAME=your_production_deployment
AZURE_OPENAI_MODEL_NAME=gpt-4

# Optional: Database persistence
CHROMA_DB_PATH=/data/chroma_db
TEMP_UPLOAD_PATH=/data/temp_uploads

# Optional: Logging
LOG_LEVEL=INFO
LOG_FILE=/var/log/rag_chatbot.log
```

#### Security Considerations

1. **API Key Security:**
   - Use environment variables, never hardcode keys
   - Rotate API keys regularly
   - Use Azure Key Vault for production

2. **File Upload Security:**
   - Validate file types and sizes
   - Scan uploaded files for malware
   - Use temporary storage with cleanup

3. **Network Security:**
   - Use HTTPS in production
   - Implement rate limiting
   - Add authentication if needed

#### Performance Optimization

1. **Vector Database:**
   - Use persistent storage for ChromaDB
   - Consider database backups
   - Monitor database size and performance

2. **Memory Management:**
   - Implement conversation history limits
   - Clean up old sessions periodically
   - Monitor memory usage

3. **Caching:**
   - Cache frequently accessed documents
   - Implement response caching for common queries
   - Use CDN for static assets

## 🔍 Troubleshooting

### Common Issues and Solutions

#### 1. Azure OpenAI Connection Issues

**Problem**: `❌ Azure OpenAI connection failed`

**Solutions:**
```bash
# Check environment variables
python -c "import os; print('API Key:', bool(os.getenv('AZURE_OPENAI_API_KEY'))); print('Endpoint:', os.getenv('AZURE_OPENAI_ENDPOINT'))"

# Test connection manually
python -c "from src.azure_openai_client import AzureOpenAIClient; client = AzureOpenAIClient(); print(client.test_connection())"
```

**Common causes:**
- Incorrect API key or endpoint
- Wrong API version
- Deployment name mismatch
- Network connectivity issues

#### 2. Document Processing Errors

**Problem**: `❌ Error adding documents`

**Solutions:**
```bash
# Check file permissions
ls -la /path/to/documents

# Verify file formats
file /path/to/document.pdf

# Test document processing
python -c "from src.document_processor import read_document; print(read_document('test.pdf')[:100])"
```

**Common causes:**
- Unsupported file formats
- Corrupted files
- Permission issues
- Large file sizes

#### 3. ChromaDB Issues

**Problem**: Vector database errors

**Solutions:**
```bash
# Check ChromaDB directory
ls -la chroma_db/

# Reset database if corrupted
python -c "from src.rag_chatbot import RAGChatbot; bot = RAGChatbot(); bot.reset_knowledge_base()"

# Check disk space
df -h
```

#### 4. Memory Issues

**Problem**: High memory usage or crashes

**Solutions:**
- Reduce chunk size in document processing
- Limit conversation history length
- Clear old sessions regularly
- Monitor system resources

#### 5. Streamlit Issues

**Problem**: Web interface not loading

**Solutions:**
```bash
# Check if port is available
netstat -an | grep 8501

# Run with different port
streamlit run streamlit_app.py --server.port=8502

# Check Streamlit logs
streamlit run streamlit_app.py --logger.level=debug
```
