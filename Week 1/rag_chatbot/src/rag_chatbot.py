from typing import Tuple, List
from .vector_database import VectorDatabase
from .azure_openai_client import AzureOpenAIClient
from .conversation_memory import ConversationMemory
from .document_processor import process_and_add_documents


class RAGChatbot:
    def __init__(self, persist_directory: str = "chroma_db"):
        self.vector_db = VectorDatabase(persist_directory)
        self.openai_client = AzureOpenAIClient()
        self.memory = ConversationMemory()

        print("RAG Chatbot initialized successfully!")

        if self.openai_client.test_connection():
            print("✓ Azure OpenAI connection successful")
        else:
            print("✗ Azure OpenAI connection failed - check your configuration")

    def add_documents(self, folder_path: str):
        collection = self.vector_db.get_collection()
        process_and_add_documents(collection, folder_path)

        info = self.vector_db.get_collection_info()
        print(
            f"Knowledge base now contains {info.get('total_documents', 0)} document chunks")

    def create_session(self) -> str:
        return self.memory.create_session()

    def query(self, question: str, session_id: str, n_chunks: int = 3) -> Tuple[str, List[str]]:
        try:
            conversation_history = self.memory.format_history_for_prompt(
                session_id)

            contextualized_query = self.openai_client.contextualize_query(
                question, conversation_history
            )

            search_results = self.vector_db.semantic_search(
                contextualized_query, n_chunks)
            context, sources = self.vector_db.get_context_with_sources(
                search_results)

            response = self.openai_client.generate_response(
                contextualized_query, context, conversation_history
            )

            self.memory.add_message(session_id, "user", question)
            self.memory.add_message(session_id, "assistant", response)

            return response, sources

        except Exception as e:
            error_response = f"I apologize, but I encountered an error while processing your question: {str(e)}"
            self.memory.add_message(session_id, "user", question)
            self.memory.add_message(session_id, "assistant", error_response)
            return error_response, []

    def simple_query(self, question: str, n_chunks: int = 3) -> Tuple[str, List[str]]:
        temp_session = self.create_session()
        return self.query(question, temp_session, n_chunks)

    def get_conversation_history(self, session_id: str) -> List[dict]:
        return self.memory.get_conversation_history(session_id)

    def clear_conversation(self, session_id: str):
        self.memory.clear_session(session_id)

    def get_knowledge_base_info(self) -> dict:
        return self.vector_db.get_collection_info()

    def reset_knowledge_base(self):
        self.vector_db.reset_collection()
        print("Knowledge base has been reset")

    def search_documents(self, query: str, n_results: int = 5) -> dict:
        return self.vector_db.semantic_search(query, n_results)

    def print_search_results(self, query: str, n_results: int = 5):
        results = self.search_documents(query, n_results)
        self.vector_db.print_search_results(results)

    def get_session_info(self, session_id: str) -> dict:
        return self.memory.get_session_info(session_id)

    def list_sessions(self) -> List[str]:
        return self.memory.list_sessions()

    def get_session_summary(self, session_id: str) -> str:
        return self.memory.get_session_summary(session_id)
