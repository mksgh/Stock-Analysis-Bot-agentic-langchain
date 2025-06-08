import os
from typing import Any
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from utils.config_loader import load_config
from langchain_groq import ChatGroq

class ModelLoader:
    """
    A utility class to load embedding models and LLM models.
    """

    def __init__(self) -> None:
        """
        Initializes the ModelLoader by loading environment variables and configuration.
        """
        load_dotenv()
        self._validate_env()
        self.config: dict = load_config()
        self.groq_api_key: str = os.getenv("GROQ_API_KEY")

    def _validate_env(self) -> None:
        """
        Validates the presence of necessary environment variables.
        Raises an EnvironmentError if any required variable is missing.
        """
        required_vars = ["GOOGLE_API_KEY", "GROQ_API_KEY"]
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        if missing_vars:
            raise EnvironmentError(f"Missing environment variables: {missing_vars}")

    def load_embeddings(self) -> GoogleGenerativeAIEmbeddings:
        """
        Loads and returns the embedding model.

        Returns
        -------
        GoogleGenerativeAIEmbeddings
            The initialized embedding model.
        """
        print("Loading Embedding model")
        model_name: str = self.config["embedding_model"]["model_name"]
        return GoogleGenerativeAIEmbeddings(model=model_name)

    def load_llm(self) -> ChatGroq:
        """
        Loads and returns the LLM model.

        Returns
        -------
        ChatGroq
            The initialized LLM model.
        """
        print("LLM loading...")
        model_name: str = self.config["llm"]["groq"]["model_name"]
        print("******this is my key*****")
        print(self.groq_api_key)
        groq_model: ChatGroq = ChatGroq(model=model_name, api_key=self.groq_api_key)
        print(groq_model.invoke("hi"))
        return groq_model  # Placeholder for future LLM loading