import os
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI

load_dotenv()


class Config:
    """Configuration class for Azure OpenAI and system settings"""

    AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
    AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
    AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")
    AZURE_OPENAI_DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")

    print(AZURE_OPENAI_API_KEY, AZURE_OPENAI_API_VERSION,
          AZURE_OPENAI_DEPLOYMENT_NAME, AZURE_OPENAI_ENDPOINT)

    MAX_SEARCH_RESULTS = 5
    MAX_FILE_SIZE_MB = 10
    SUPPORTED_FILE_TYPES = ['.txt', '.md', '.pdf']


def get_azure_model(temperature: float = 0.1) -> AzureChatOpenAI:
    """Create an Azure OpenAI model instance"""
    if not Config.AZURE_OPENAI_ENDPOINT or not Config.AZURE_OPENAI_API_KEY:
        raise ValueError(
            "Azure OpenAI configuration is missing. Please check your .env file.")

    return AzureChatOpenAI(
        azure_endpoint=Config.AZURE_OPENAI_ENDPOINT,
        api_key=Config.AZURE_OPENAI_API_KEY,
        api_version=Config.AZURE_OPENAI_API_VERSION,
        azure_deployment=Config.AZURE_OPENAI_DEPLOYMENT_NAME,
        temperature=temperature
    )
