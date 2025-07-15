# Multi-Agent Support System

A sophisticated support system built with LangGraph and Azure OpenAI that intelligently routes user queries to specialized agents for IT and Finance support.

▶️ **Watch the system in action:**  

https://github.com/user-attachments/assets/c629bc1e-0c15-4cac-b5a5-ad1ad1fe5c19

## 🏗️ System Architecture

The system consists of three specialized agents working together:

### 1. **Supervisor Agent** 🎯

- **Role**: Query classification and routing
- **Model**: Azure OpenAI GPT-4
- **Function**: Analyzes user queries and routes them to appropriate specialist agents
- **Routing Logic**:
  - IT queries → IT Agent
  - Finance queries → Finance Agent

### 2. **IT Agent** 💻

- **Role**: Technical support specialist
- **Model**: Azure OpenAI GPT-4
- **Tools**:
  - `ReadFile`: Access internal IT documentation
  - `WebSearch`: Search external IT resources using DuckDuckGo
  - `Handoffs`: Transfer to other agents when needed
- **Expertise**: VPN setup, software approval, hardware requests, troubleshooting

### 3. **Finance Agent** 💰

- **Role**: Financial support specialist  
- **Model**: Azure OpenAI GPT-4
- **Tools**:
  - `ReadFile`: Access internal finance documentation
  - `WebSearch`: Search external finance resources using DuckDuckGo
  - `Handoffs`: Transfer to other agents when needed
- **Expertise**: Reimbursements, payroll, budgets, expense policies

## 🚀 Features

- **Intelligent Routing**: LLM-powered query classification
- **Contextual Tools**: Each agent has access to relevant internal docs and web search
- **Seamless Handoffs**: Smooth transitions between agents with context preservation
- **Azure OpenAI Integration**: Enterprise-grade AI with security and compliance
- **DuckDuckGo Search**: Free web search without API keys
- **Document Processing**: Support for PDF, Markdown, and text files
- **Modern Streamlit UI**: Native chat interface with quick-start buttons
- **Error Handling**: Robust error management and fallback mechanisms

## 📁 Project Structure

```
multi-agent-support/
├── main.py                     
├── streamlit_app.py            
├── run_streamlit.py           
├── config.py                  
├── requirements.txt          
├── .env.example              
├── agents/
│   ├── __init__.py
│   ├── supervisor.py         
│   ├── it_agent.py          
│   └── finance_agent.py     
├── tools/
│   ├── __init__.py
│   ├── read_file.py          
│   └── web_search.py       
├── utils/
│   ├── __init__.py
│   └── handoffs.py           
└── data/
    ├── it_docs/            
    │   ├── vpn_setup_guide.md
    │   ├── approved_software_list.md
    │   └── hardware_request_process.md
    └── finance_docs/        
        ├── reimbursement_policy.md
        └── payroll_schedule.md
```

## 🛠️ Installation

### Prerequisites

- Python 3.8+
- Azure OpenAI account and API key
- Internet connection for web search

### Setup Steps

1. **Clone the repository**

   ```bash
   git clone https://github.com/Ayushi760/Innovation-Sprint-2025
   cd multi-agent-support
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Azure OpenAI**

   ```bash
   cp .env.example .env
   ```

   Edit `.env` with your Azure OpenAI credentials:

   ```env
   AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
   AZURE_OPENAI_API_KEY=your-api-key-here
   AZURE_OPENAI_API_VERSION=2024-02-15-preview
   AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o
   ```

4. **Run the system**

   **Option A: Streamlit Web UI**

   ```bash
   streamlit run app.py
   ```

## 🎮 Usage

### Streamlit Web UI

Run the modern web interface for the best user experience:

```bash
streamlit run app.py
```

The web interface provides:

- 🎨 **Modern Chat Interface**: Native Streamlit chat components
- 💡 **Quick Start Buttons**: Sample queries in main chat window
- 🤖 **Agent Information**: Tabbed sidebar with agent details
- 📊 **System Status**: Live metrics and health indicators
- ⚙️ **Smart Controls**: Clear chat, system info, and help sections
- 📱 **Responsive Design**: Works on all devices

Access the application at: <http://localhost:8501>

## 🔧 Configuration

### Azure OpenAI Models

- **GPT-4**: Supervisor and specialist agents

### File Processing

- **Supported formats**: PDF, Markdown (.md), Text (.txt)
- **File size limit**: 10MB per file
- **Search capability**: Keyword-based file discovery

### Web Search

- **Provider**: DuckDuckGo (no API key required)
- **Results limit**: 5 results per query
- **Context enhancement**: Query optimization based on agent domain

## 📚 Sample Queries

### IT Support Examples

- "How do I set up VPN?"
- "What software is approved for use?"
- "How to request a new laptop?"
- "My computer won't connect to WiFi"
- "How do I install Visual Studio Code?"

### Finance Support Examples

- "How to file a reimbursement?"
- "Where to find last month's budget report?"
- "When is payroll processed?"
- "What's the meal allowance for business travel?"
- "How do I submit expense reports?"

## 🔄 Agent Workflow

1. **User Query** → **Supervisor Agent**
2. **Classification** → IT or Finance determination
3. **Handoff** → Route to appropriate specialist
4. **Tool Usage** → ReadFile for internal docs, WebSearch for external info
5. **Response** → Specialist provides comprehensive answer
6. **Return** → Back to user with complete solution
