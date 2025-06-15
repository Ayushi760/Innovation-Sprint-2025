import streamlit as st
import os
import time
from src.rag_chatbot import RAGChatbot
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="🧠 AI Knowledge Assistant",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

if 'chatbot' not in st.session_state:
    st.session_state.chatbot = None
if 'session_id' not in st.session_state:
    st.session_state.session_id = None
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'initialized' not in st.session_state:
    st.session_state.initialized = False

def initialize_chatbot():
    try:
        progress_container = st.container()
        with progress_container:
            st.info("🚀 Initializing your AI Knowledge Assistant...")
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            steps = [
                (20, "📶 Connecting to Azure OpenAI..."),
                (40, "📚 Loading vector database..."),
                (60, "🧠 Initializing AI models..."),
                (80, "⚡ Setting up conversation memory..."),
                (100, "✨ Finalizing setup...")
            ]
            
            for progress, message in steps:
                progress_bar.progress(progress)
                status_text.text(message)
                time.sleep(0.3)
            
            chatbot = RAGChatbot()
            session_id = chatbot.create_session()
            st.session_state.chatbot = chatbot
            st.session_state.session_id = session_id
            st.session_state.initialized = True
            
            progress_container.empty()
            
            st.success("🎉 AI Knowledge Assistant is ready to help you!")
            st.balloons()
            return True
            
    except Exception as e:
        st.error(f"❌ Failed to initialize: {str(e)}")
        st.error("Please check your Azure OpenAI configuration in the .env file")
        return False

def display_welcome_header():
    st.markdown("# 🧠 AI Knowledge Assistant")
    st.markdown("### Your intelligent document companion powered by Azure OpenAI")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("📚 **Smart Document Analysis**\nUpload and query your documents intelligently")
    
    with col2:
        st.info("💬 **Conversational AI**\nNatural language interactions with context memory")
    
    with col3:
        st.info("🔍 **Source Attribution**\nGet answers with referenced sources")
    
    st.markdown("---")

def display_sidebar():
    with st.sidebar:
        st.markdown("# ⚙️ Control Panel")
        
        tab1, tab2, tab3 = st.tabs(["🔧 Setup", "📚 Knowledge", "💬 Session"])
        
        with tab1:
            st.markdown("### Configuration Status")
            
            # Check environment variables
            required_vars = [
                "AZURE_OPENAI_API_KEY",
                "AZURE_OPENAI_ENDPOINT", 
                "AZURE_OPENAI_DEPLOYMENT_NAME"
            ]
            
            missing_vars = [var for var in required_vars if not os.getenv(var)]
            
            if missing_vars:
                st.error("❌ **Configuration Issues**")
                with st.expander("Missing Variables", expanded=True):
                    for var in missing_vars:
                        st.write(f"• `{var}`")
                st.info("💡 Create a `.env` file with your Azure OpenAI credentials")
                return False
            else:
                st.success("✅ **Configuration Valid**")
                st.write("All required environment variables are set")
            
            st.markdown("---")
            
            # Initialize chatbot section
            if not st.session_state.initialized:
                st.markdown("### Initialize Assistant")
                if st.button("🚀 **Start AI Assistant**", type="primary", use_container_width=True):
                    initialize_chatbot()
            else:
                st.success("✅ **Assistant Ready**")
                st.write("Your AI assistant is active and ready")
        
        with tab2:
            if st.session_state.initialized:
                st.markdown("### Document Management")
                
                # Knowledge base metrics
                if st.session_state.chatbot:
                    kb_info = st.session_state.chatbot.get_knowledge_base_info()
                    total_docs = kb_info.get('total_documents', 0)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("📄 Documents", total_docs)
                    with col2:
                        st.metric("🔍 Status", "Active" if total_docs > 0 else "Empty")
                
                st.markdown("---")
                
                # File upload section
                st.markdown("### Upload Documents")
                uploaded_files = st.file_uploader(
                    "Choose files to add to knowledge base",
                    type=['pdf', 'docx', 'txt'],
                    accept_multiple_files=True,
                    help="Supported formats: PDF, DOCX, TXT"
                )
                
                if uploaded_files:
                    st.info(f"📁 {len(uploaded_files)} file(s) selected")
                    
                    if st.button("**Add to Knowledge Base**", type="secondary", use_container_width=True):
                        with st.spinner("Processing documents..."):
                            # Save uploaded files temporarily
                            temp_dir = "temp_uploads"
                            os.makedirs(temp_dir, exist_ok=True)
                            
                            for uploaded_file in uploaded_files:
                                file_path = os.path.join(temp_dir, uploaded_file.name)
                                with open(file_path, "wb") as f:
                                    f.write(uploaded_file.getbuffer())
                            
                            # Add documents to knowledge base
                            try:
                                st.session_state.chatbot.add_documents(temp_dir)
                                st.success(f"✅ Added {len(uploaded_files)} documents!")
                                st.rerun()
                                
                                # Clean up temp files
                                import shutil
                                shutil.rmtree(temp_dir)
                            except Exception as e:
                                st.error(f"❌ Error: {str(e)}")
            else:
                st.info("Initialize the assistant first to manage documents")
        
        with tab3:
            if st.session_state.initialized:
                st.markdown("### Session Control")
                
                # Session info
                if st.session_state.session_id:
                    st.info(f"🆔 Session: `{st.session_state.session_id[:8]}...`")
                
                # Session actions
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("🔄 **New Session**", use_container_width=True):
                        st.session_state.session_id = st.session_state.chatbot.create_session()
                        st.session_state.messages = []
                        st.success("✅ New session created")
                        st.rerun()
                
                with col2:
                    if st.button("🗑️ **Clear Chat**", use_container_width=True):
                        if st.session_state.session_id:
                            st.session_state.chatbot.clear_conversation(st.session_state.session_id)
                            st.session_state.messages = []
                            st.success("✅ Chat cleared")
                            st.rerun()
                
                st.markdown("---")
                
                # Chat statistics
                if st.session_state.messages:
                    user_msgs = len([m for m in st.session_state.messages if m["role"] == "user"])
                    ai_msgs = len([m for m in st.session_state.messages if m["role"] == "assistant"])
                    
                    st.markdown("### Chat Statistics")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("� Your Messages", user_msgs)
                    with col2:
                        st.metric("🤖 AI Responses", ai_msgs)
            else:
                st.info("Initialize the assistant first to manage sessions")
        
        return True

def display_chat_interface():
    """Display the main chat interface"""
    if not st.session_state.initialized:
        # Welcome screen when not initialized
        st.container()
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("### 🚀 Getting Started")
            st.info("Please initialize your AI Knowledge Assistant using the **Setup** tab in the sidebar to begin chatting.")
            st.markdown("#### What you can do:")
            st.markdown("- 📚 Upload documents (PDF, DOCX, TXT)")
            st.markdown("- 💬 Ask questions about your documents")
            st.markdown("- 🔍 Get answers with source references")
            st.markdown("- 🧠 Have contextual conversations")
        return
    
    # Chat messages container
    chat_container = st.container()
    
    with chat_container:
        # Display existing messages
        for i, message in enumerate(st.session_state.messages):
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                
                # Display sources if available
                if "sources" in message and message["sources"]:
                    with st.expander("📚 **View Sources**", expanded=False):
                        for j, source in enumerate(message["sources"], 1):
                            st.markdown(f"**{j}.** `{source}`")
    
    # Chat input
    if prompt := st.chat_input("📄 Ask me anything about your documents...", key="chat_input"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message immediately
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate and display assistant response
        with st.chat_message("assistant"):
            with st.spinner("🤔 Thinking..."):
                try:
                    response, sources = st.session_state.chatbot.query(
                        prompt, 
                        st.session_state.session_id
                    )
                    
                    # Display the response
                    st.markdown(response)
                    
                    # Display sources if available
                    if sources:
                        with st.expander("📚 **View Sources**", expanded=False):
                            for j, source in enumerate(sources, 1):
                                st.markdown(f"**{j}.** `{source}`")
                    
                    # Add assistant response to chat history
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": response,
                        "sources": sources
                    })
                    
                except Exception as e:
                    error_msg = f"❌ I encountered an error: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": error_msg
                    })

def main():
    """Main application function"""
    # Display header
    display_welcome_header()
    
    # Display sidebar and check if configuration is valid
    config_valid = display_sidebar()
    
    if not config_valid:
        # Show configuration help in main area
        st.error("⚠️ **Configuration Required**")
        st.markdown("Please set up your Azure OpenAI credentials to continue.")
        
        with st.expander("🔧 **Setup Instructions**", expanded=True):
            st.markdown("""
            1. Create a `.env` file in your project directory
            2. Add the following variables:
            ```
            AZURE_OPENAI_API_KEY=your_api_key_here
            AZURE_OPENAI_ENDPOINT=your_endpoint_here
            AZURE_OPENAI_DEPLOYMENT_NAME=your_deployment_name_here
            ```
            3. Restart the application
            """)
        return
    
    display_chat_interface()

if __name__ == "__main__":
    main()
