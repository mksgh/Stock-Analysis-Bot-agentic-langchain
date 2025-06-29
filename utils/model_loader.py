import sys

sys.path.append("../")

import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_openai import AzureOpenAIEmbeddings, AzureChatOpenAI
from utils.config_loader import load_config
from langchain_groq import ChatGroq


class ModelLoader:
    """
    Utility class for loading embedding models and large language models (LLMs)
    from different providers (Azure, Google, Groq) based on configuration and environment variables.

    This class ensures all required environment variables are set and provides
    methods to instantiate embedding and LLM objects for downstream use.
    """

    def __init__(self) -> None:
        """
        Initializes the ModelLoader by loading environment variables and configuration.

        Loads environment variables from a .env file, validates the presence of required
        variables, and loads the configuration from the config file. Also sets up
        provider-specific environment variables for Azure.
        """
        load_dotenv()
        self._validate_env()
        self.config: dict = load_config()
        self.groq_api_key: str = os.getenv("GROQ_API_KEY")
        os.environ["AZURE_OPENAI_API_KEY"] = os.getenv("AZURE_OPENAI_API_KEY")  # type: ignore
        os.environ["AZURE_OPENAI_ENDPOINT"] = os.getenv("AZURE_OPENAI_ENDPOINT")  # type: ignore

    def _validate_env(self) -> None:
        """
        Validates the presence of necessary environment variables.

        Raises
        ------
        EnvironmentError
            If any required environment variable is missing.
        """
        required_vars = [
            "GOOGLE_API_KEY",
            "GROQ_API_KEY",
            "AZURE_OPENAI_API_KEY",
            "AZURE_OPENAI_ENDPOINT",
        ]
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        if missing_vars:
            raise EnvironmentError(f"Missing environment variables: {missing_vars}")

    def load_embeddings(self) -> GoogleGenerativeAIEmbeddings:
        """
        Loads and returns the embedding model based on the configured provider.

        Returns
        -------
        GoogleGenerativeAIEmbeddings or AzureOpenAIEmbeddings
            The initialized embedding model for the selected provider.

        Raises
        ------
        KeyError
            If the provider specified in the config is not supported.
        """
        model_provider: str = self.config["model_provider"]["provider"]
        print(f"Embedding model provider: {model_provider}")

        if model_provider == "azure":
            print("Loading Embedding model...")
            model_name: str = self.config["embedding_model"]["azure"]["model_name"]
            return AzureOpenAIEmbeddings(model=model_name)

        elif model_provider == "google":
            print("Loading Embedding model...")
            model_name: str = self.config["embedding_model"]["google"]["model_name"]
            return GoogleGenerativeAIEmbeddings(model=model_name)

        elif model_provider == "groq":
            print("Loading Embedding model...")
            model_name: str = self.config["embedding_model"]["groq"]["model_name"]
            return GoogleGenerativeAIEmbeddings(model=model_name)

        else:
            raise KeyError(f"Unsupported embedding model provider: {model_provider}")

    def load_llm(self) -> ChatGroq:
        """
        Loads and returns the LLM (large language model) based on the configured provider.

        Returns
        -------
        ChatGroq, AzureChatOpenAI, or ChatGoogleGenerativeAI
            The initialized LLM for the selected provider.

        Raises
        ------
        KeyError
            If the provider specified in the config is not supported.
        """
        print("LLM loading...")
        model_provider: str = self.config["model_provider"]["provider"]
        print(f"Model provider: {model_provider}")

        if model_provider == "groq":
            model_name: str = self.config["llm"]["groq"]["model_name"]
            print(
                f"Loading groq LLM: '{model_name}' with API key '{self.groq_api_key}'"
            )
            groq_model: ChatGroq = ChatGroq(model=model_name, api_key=self.groq_api_key)
            return groq_model

        elif model_provider == "azure":
            model_name: str = self.config["llm"]["azure"]["model_name"]
            api_version: str = self.config["llm"]["azure"]["api_version"]
            print(f"Loading Azure LLM: '{model_name}' with API version '{api_version}'")
            return AzureChatOpenAI(
                azure_deployment=model_name,
                api_version=api_version,
            )

        elif model_provider == "google":
            model_name: str = self.config["llm"]["google"]["model_name"]
            print(f"Loading Google LLM: '{model_name}'")
            return ChatGoogleGenerativeAI(model=model_name)

        else:
            raise KeyError(f"Unsupported LLM provider: {model_provider}")
