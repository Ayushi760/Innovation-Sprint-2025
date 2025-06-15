import os
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()


class AzureOpenAIClient:
    def __init__(self):
        self.client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version=os.getenv(
                "AZURE_OPENAI_API_VERSION", "2024-02-15-preview"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
        )
        self.deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
        self.model_name = os.getenv("AZURE_OPENAI_MODEL_NAME", "gpt-4")

    def get_prompt(self, context: str, conversation_history: str, query: str) -> str:
        """Generate a prompt combining context, history, and query"""
        prompt = f"""Based on the following context and conversation history, 
        please provide a relevant and contextual response. If the answer cannot 
        be derived from the context, only use the conversation history or say 
        "I cannot answer this based on the provided information."

        Context from documents:
        {context}

        Previous conversation:
        {conversation_history}

        Human: {query}

        Assistant:"""

        return prompt

    def generate_response(self, query: str, context: str, conversation_history: str = "") -> str:
        """Generate a response using Azure OpenAI with conversation history"""
        prompt = self.get_prompt(context, conversation_history, query)

        try:
            response = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that answers questions based on the provided context."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0,
                max_tokens=500
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating response: {str(e)}"

    def contextualize_query(self, query: str, conversation_history: str) -> str:
        # If no conversation history, return original query
        if not conversation_history.strip():
            return query

        contextualize_prompt = """Given a chat history and the latest user question 
        which might reference context in the chat history, formulate a standalone 
        question which can be understood without the chat history. Do NOT answer 
        the question, just reformulate it if needed and otherwise return it as is."""

        try:
            completion = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=[
                    {"role": "system", "content": contextualize_prompt},
                    {"role": "user", "content": f"Chat history:\n{conversation_history}\n\nQuestion:\n{query}"}
                ],
                temperature=0,
                max_tokens=200
            )
            return completion.choices[0].message.content
        except Exception as e:
            print(
                f"Warning: Could not contextualize query ({str(e)}). Using original query.")
            return query

    def test_connection(self) -> bool:
        try:
            response = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=[
                    {"role": "user", "content": "Hello, this is a test."}],
                max_tokens=10
            )
            return True
        except Exception as e:
            print(f"Connection test failed: {str(e)}")
            return False
