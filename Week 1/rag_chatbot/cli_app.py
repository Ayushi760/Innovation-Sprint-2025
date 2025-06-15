import os
from dotenv import load_dotenv
from src.rag_chatbot import RAGChatbot

load_dotenv()


class RAGChatbotCLI:
    def __init__(self):
        self.chatbot = None
        self.session_id = None

    def check_environment(self):
        required_vars = [
            "AZURE_OPENAI_API_KEY",
            "AZURE_OPENAI_ENDPOINT",
            "AZURE_OPENAI_DEPLOYMENT_NAME"
        ]

        missing_vars = [var for var in required_vars if not os.getenv(var)]

        if missing_vars:
            print("❌ Missing environment variables:")
            for var in missing_vars:
                print(f"   - {var}")
            print("\nPlease create a .env file with your Azure OpenAI credentials")
            print("Use .env.example as a template")
            return False

        return True

    def initialize_chatbot(self):
        try:
            print("🚀 Initializing RAG Chatbot...")
            self.chatbot = RAGChatbot()
            self.session_id = self.chatbot.create_session()
            print("✅ RAG Chatbot initialized successfully!")
            return True
        except Exception as e:
            print(f"❌ Failed to initialize chatbot: {str(e)}")
            print("Please check your Azure OpenAI configuration")
            return False

    def print_help(self):
        print("\n📋 Available Commands:")
        print("  /help          - Show this help message")
        print("  /add <path>    - Add documents from folder to knowledge base")
        print("  /info          - Show knowledge base information")
        print("  /search <query> - Search documents without generating response")
        print("  /clear         - Clear conversation history")
        print("  /new           - Start new conversation session")
        print("  /history       - Show conversation history")
        print("  /quit or /exit - Exit the chatbot")
        print("  <message>      - Ask a question to the chatbot")
        print()

    def handle_command(self, command):
        parts = command.strip().split(' ', 1)
        cmd = parts[0].lower()
        arg = parts[1] if len(parts) > 1 else ""

        if cmd == "/help":
            self.print_help()

        elif cmd == "/add":
            if not arg:
                print("❌ Please specify a folder path: /add <path>")
                return

            if not os.path.exists(arg):
                print(f"❌ Folder '{arg}' does not exist")
                return

            print(f"📤 Adding documents from '{arg}'...")
            try:
                self.chatbot.add_documents(arg)
                print("✅ Documents added successfully!")
            except Exception as e:
                print(f"❌ Error adding documents: {str(e)}")

        elif cmd == "/info":
            info = self.chatbot.get_knowledge_base_info()
            print(f"📊 Knowledge Base Information:")
            print(
                f"   Total document chunks: {info.get('total_documents', 0)}")
            print(f"   Collection name: {info.get('collection_name', 'N/A')}")

        elif cmd == "/search":
            if not arg:
                print("❌ Please specify a search query: /search <query>")
                return

            print(f"🔍 Searching for: '{arg}'")
            self.chatbot.print_search_results(arg)

        elif cmd == "/clear":
            self.chatbot.clear_conversation(self.session_id)
            print("✅ Conversation history cleared")

        elif cmd == "/new":
            self.session_id = self.chatbot.create_session()
            print("✅ New conversation session started")

        elif cmd == "/history":
            history = self.chatbot.get_conversation_history(self.session_id)
            if not history:
                print("📝 No conversation history")
                return

            print("📝 Conversation History:")
            for i, msg in enumerate(history, 1):
                role = "You" if msg["role"] == "user" else "Bot"
                print(f"   {i}. {role}: {msg['content'][:100]}...")

        elif cmd in ["/quit", "/exit"]:
            print("👋 Goodbye!")
            return False

        else:
            print(f"❌ Unknown command: {cmd}")
            print("Type /help for available commands")

        return True

    def run(self):
        print("🤖 RAG-based Chatbot with Azure OpenAI")
        print("=" * 50)

        if not self.check_environment():
            return

        if not self.initialize_chatbot():
            return

        print("\n💡 Type /help for available commands")
        print("💬 Start asking questions about your documents!")
        print("🚪 Type /quit to exit\n")

        while True:
            try:
                user_input = input("You: ").strip()

                if not user_input:
                    continue

                if user_input.startswith('/'):
                    if not self.handle_command(user_input):
                        break
                    continue

                print("🤔 Thinking...")
                try:
                    response, sources = self.chatbot.query(
                        user_input, self.session_id)

                    print(f"\n🤖 Bot: {response}")

                    if sources:
                        print(f"\n📚 Sources:")
                        for source in sources:
                            print(f"   • {source}")

                    print()

                except Exception as e:
                    print(f"❌ Error: {str(e)}")
                    print()

            except KeyboardInterrupt:
                print("\n\n👋 See you soon!")
                break
            except EOFError:
                print("\n\n👋 See you soon!")
                break


def main():
    cli = RAGChatbotCLI()
    cli.run()


if __name__ == "__main__":
    main()
