import streamlit as st
from datetime import datetime
from main import create_support_system, run_query
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="Multi-Agent Support System",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


def initialize_session_state():
    """Initialize session state variables"""
    if 'support_system' not in st.session_state:
        st.session_state.support_system = None
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'system_initialized' not in st.session_state:
        st.session_state.system_initialized = False


def check_configuration():
    """Check if Azure OpenAI is properly configured"""
    required_vars = [
        "AZURE_OPENAI_ENDPOINT",
        "AZURE_OPENAI_API_KEY",
        "AZURE_OPENAI_DEPLOYMENT_NAME"
    ]

    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)

    return len(missing_vars) == 0, missing_vars


def initialize_support_system():
    """Initialize the support system"""
    try:
        if st.session_state.support_system is None:
            with st.spinner("🔄 Initializing Multi-Agent Support System..."):
                st.session_state.support_system = create_support_system()
                st.session_state.system_initialized = True
        return True
    except Exception as e:
        st.error(f"❌ Failed to initialize support system: {str(e)}")
        return False


def display_agent_info():
    """Display information about the agents"""
    st.sidebar.markdown("### 🤖 **AI Agents**")

    tab1, tab2, tab3 = st.sidebar.tabs(["🎯", "💻", "💰"])

    with tab1:
        st.markdown("**Supervisor**")
        st.caption("Query Router & AI Classifier")
        st.info("🧠 Routes your questions to the right specialist using advanced AI")

    with tab2:
        st.markdown("**IT Support**")
        st.caption("Technical Specialist")
        with st.container():
            st.markdown("**Expertise:**")
            st.markdown("• 🔐 VPN & Security")
            st.markdown("• 📱 Software & Apps")
            st.markdown("• 💻 Hardware Support")
            st.markdown("• 🔧 Troubleshooting")

    with tab3:
        st.markdown("**Finance**")
        st.caption("Financial Specialist")
        with st.container():
            st.markdown("**Expertise:**")
            st.markdown("• 💳 Reimbursements")
            st.markdown("• 💰 Payroll & Benefits")
            st.markdown("• 📊 Reports & Budgets")
            st.markdown("• 📋 Policies & Procedures")


def display_sidebar_stats():
    """Display system statistics and status"""
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 **System Status**")

    col1, col2 = st.sidebar.columns(2)

    with col1:
        st.metric(
            label="🤖 Agents",
            value="3",
            help="Active AI agents ready to help"
        )

    with col2:
        st.metric(
            label="📚 Docs",
            value="5",
            help="Internal documentation files"
        )

    if st.session_state.get('system_initialized', False):
        st.sidebar.success("🟢 **System Online**")
    else:
        st.sidebar.warning("🟡 **System Initializing**")


def display_sidebar_controls():
    """Display sidebar controls and actions"""
    st.sidebar.markdown("---")
    st.sidebar.markdown("### ⚙️ **Controls**")

    if st.sidebar.button("🗑️ Clear Chat", use_container_width=True, type="secondary"):
        st.session_state.messages = []
        st.rerun()

    with st.sidebar.expander("ℹ️ System Information"):
        st.markdown("""
        **Version:** 1.0.0  
        **Framework:** LangGraph  
        **AI Model:** Azure OpenAI GPT-4  
        **Search:** DuckDuckGo  
        **Interface:** Streamlit  
        """)

    with st.sidebar.expander("❓ Need Help?"):
        st.markdown("""
        **Getting Started:**
        1. Click quick start buttons
        2. Type your question
        3. Get instant AI support
        
        **Tips:**
        • Be specific in your questions
        • Mention IT or Finance context
        • Ask follow-up questions
        """)


def display_quick_queries():
    """Display quick query buttons in the main chat area"""
    st.markdown("### 💡 **Quick Start - Try These Questions:**")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**💻 IT Support**")

        it_samples = [
            ("🔐 VPN Setup", "How do I set up VPN?"),
            ("📱 Software Approval", "What software is approved for use?"),
            ("💻 Hardware Request", "How to request a new laptop?"),
            ("🌐 WiFi Troubleshooting", "My computer won't connect to WiFi")
        ]

        for label, query in it_samples:
            if st.button(label, key=f"it_{query}", use_container_width=True):
                st.session_state.messages.append(
                    {"role": "user", "content": query})
                process_query(query)
                st.rerun()

    with col2:
        st.markdown("**💰 Finance Support**")

        finance_samples = [
            ("💳 File Reimbursement", "How to file a reimbursement?"),
            ("💰 Payroll Schedule", "When is payroll processed?"),
            ("📊 Budget Reports", "Where to find budget reports?"),
            ("🍽️ Travel Allowance", "What's the meal allowance for travel?")
        ]

        for label, query in finance_samples:
            if st.button(label, key=f"finance_{query}", use_container_width=True):
                st.session_state.messages.append(
                    {"role": "user", "content": query})
                process_query(query)
                st.rerun()

    st.markdown("---")


def process_query(query):
    """Process a user query and add response to messages"""
    try:
        with st.spinner("🔄 Processing your query..."):
            response = run_query(st.session_state.support_system, query)
            st.session_state.messages.append(
                {"role": "assistant", "content": response})
    except Exception as e:
        error_msg = f"❌ Error processing query: {str(e)}"
        st.session_state.messages.append(
            {"role": "assistant", "content": error_msg})


def main():
    initialize_session_state()

    st.title("🤖 Multi-Agent Support System")
    st.markdown("*Powered by Azure OpenAI and LangGraph*")

    display_agent_info()
    display_sidebar_stats()
    display_sidebar_controls()

    config_ok, missing_vars = check_configuration()

    if not config_ok:
        st.error("❌ **Configuration Error**")
        st.error(
            "Azure OpenAI configuration is missing. Please check your .env file.")
        st.error(f"**Missing variables:** {', '.join(missing_vars)}")
        st.info(
            "Please configure your .env file with the correct Azure OpenAI credentials.")
        return

    if not st.session_state.system_initialized:
        st.info(
            "🔧 **System Status**: Multi-Agent Support System is ready to initialize.")

        if st.button("🚀 Initialize System", type="primary"):
            if initialize_support_system():
                st.success(
                    "✅ **System Initialized**: Multi-Agent Support System is now ready to help you!")
                st.rerun()
            return
    else:
        st.success(
            "✅ **System Ready**: Multi-Agent Support System is initialized and ready to help!")

    if st.session_state.system_initialized:
        if not st.session_state.messages:
            display_quick_queries()

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("Ask your IT or Finance question here..."):
            st.session_state.messages.append(
                {"role": "user", "content": prompt})

            try:
                with st.spinner("🔄 Processing your query..."):
                    response = run_query(
                        st.session_state.support_system, prompt)
                st.session_state.messages.append(
                    {"role": "assistant", "content": response})
            except Exception as e:
                error_msg = f"❌ Error processing query: {str(e)}"
                st.session_state.messages.append(
                    {"role": "assistant", "content": error_msg})

            st.rerun()

        if not st.session_state.messages:
            with st.chat_message("assistant"):
                st.markdown("""
                👋 **Welcome to the Multi-Agent Support System!**
                
                I'm here to help you with:
                - 💻 **IT Support**: VPN setup, software approval, hardware requests, troubleshooting
                - 💰 **Finance Support**: Reimbursements, payroll, budgets, expense policies
                
                **Get started by clicking one of the quick questions above or type your own question below!**
                """)


if __name__ == "__main__":
    main()
