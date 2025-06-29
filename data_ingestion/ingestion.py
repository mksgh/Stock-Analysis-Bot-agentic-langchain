import os
import sys
import tempfile

from typing import List, Any
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_pinecone import PineconeVectorStore
from utils.model_loader import ModelLoader
from utils.config_loader import load_config
from pinecone import ServerlessSpec, Pinecone
from uuid import uuid4

from exception.exceptions import CustomException

class DataIngestion:
    """
    Handles document loading, transformation, and ingestion into Pinecone vector store.

    Methods
    -------
    __init__():
        Initializes the DataIngestion pipeline, loads environment variables and configuration.

    _load_env_variables():
        Loads required environment variables from .env file.

    load_documents(uploaded_files) -> List[Document]:
        Loads and parses uploaded files into LangChain Document objects.

    store_in_vector_db(documents: List[Document]):
        Splits documents and stores them in the Pinecone vector database.

    run_pipeline(uploaded_files):
        Executes the complete data ingestion pipeline: loads and parses uploaded files,
        splits them into chunks, and stores them in the Pinecone vector database.
    """

    def __init__(self) -> None:
        """
        Initializes the DataIngestion pipeline by loading the model, environment variables, and configuration.
        """
        try:
            print("Initializing DataIngestion pipeline...")
            self.model_loader: ModelLoader = ModelLoader()
            self._load_env_variables()
            self.config: dict = load_config()
        except Exception as e:
            raise CustomException(e, sys)

    def _load_env_variables(self) -> None:
        """
        Loads required environment variables from the .env file.
        Raises an error if any required variable is missing.
        """
        try:
            load_dotenv()

            required_vars = [
                "GOOGLE_API_KEY",
                "PINECONE_API_KEY",
                "AZURE_OPENAI_API_KEY",
                "AZURE_OPENAI_ENDPOINT",
            ]

            missing_vars = [var for var in required_vars if not os.getenv(var)]
            if missing_vars:
                raise EnvironmentError(f"Missing environment variables: {missing_vars}")

            self.google_api_key: str = os.getenv("GOOGLE_API_KEY")
            self.pinecone_api_key: str = os.getenv("PINECONE_API_KEY")
            os.environ["AZURE_OPENAI_API_KEY"] = os.getenv("AZURE_OPENAI_API_KEY")  # type: ignore
            os.environ["AZURE_OPENAI_ENDPOINT"] = os.getenv("AZURE_OPENAI_ENDPOINT")  # type: ignore

        except Exception as e:
            raise CustomException(e, sys)

    def load_documents(self, uploaded_files: List[Any]) -> List[Document]:
        """
        Loads and parses uploaded files into LangChain Document objects.

        Parameters
        ----------
        uploaded_files : list
            List of uploaded file objects.

        Returns
        -------
        List[Document]
            List of parsed Document objects.
        """
        try:
            documents: List[Document] = []
            for uploaded_file in uploaded_files:
                file_ext: str = os.path.splitext(uploaded_file.filename)[1].lower()
                suffix: str = file_ext if file_ext in [".pdf", ".docx"] else ".tmp"

                with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
                    temp_file.write(uploaded_file.file.read())
                    temp_path: str = temp_file.name

                if file_ext == ".pdf":
                    loader: PyPDFLoader = PyPDFLoader(temp_path)
                    documents.extend(loader.load())
                elif file_ext == ".docx":
                    loader: Docx2txtLoader = Docx2txtLoader(temp_path)
                    documents.extend(loader.load())
                else:
                    print(f"Unsupported file type: {uploaded_file.filename}")
            return documents
        except Exception as e:
            raise CustomException(e, sys)

    def store_in_vector_db(self, documents: List[Document]) -> None:
        """
        Splits documents into chunks and stores them in the Pinecone vector database.

        Parameters
        ----------
        documents : List[Document]
            List of Document objects to store.
        """
        try:
            text_splitter: RecursiveCharacterTextSplitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
                length_function=len
            )
            documents = text_splitter.split_documents(documents)

            pinecone_client: Pinecone = Pinecone(api_key=self.pinecone_api_key)
            model_provider: str = self.config["model_provider"]["provider"]

            if model_provider == "azure":
                index_name: str = self.config["vector_db"]["azure"]["index_name"]
                embedding_dimension: int = self.config["vector_db"]["azure"]["dimension"]

            elif model_provider == "google":
                index_name: str = self.config["vector_db"]["groq"]["index_name"]
                embedding_dimension: int = self.config["vector_db"]["groq"]["dimension"]

            elif model_provider == "groq":
                index_name: str = self.config["vector_db"]["groq"]["index_name"]
                embedding_dimension: int = self.config["vector_db"]["groq"]["dimension"]
            

            if index_name not in [i.name for i in pinecone_client.list_indexes()]:
                pinecone_client.create_index(
                    name=index_name,
                    dimension=embedding_dimension,  # adjust if needed based on embedding model
                    metric="cosine",
                    spec=ServerlessSpec(cloud="aws", region="us-east-1"),
                )

            index = pinecone_client.Index(index_name)
            vector_store: PineconeVectorStore = PineconeVectorStore(index=index, 
                                                                    embedding=self.model_loader.load_embeddings())
            uuids: List[str] = [str(uuid4()) for _ in range(len(documents))]

            vector_store.add_documents(documents=documents, ids=uuids)
        except Exception as e:
            raise CustomException(e, sys)

    def run_pipeline(self, uploaded_files: List[Any]) -> None:
        """
        Executes the complete data ingestion pipeline: loads and parses uploaded files,
        splits them into chunks, and stores them in the Pinecone vector database.

        Parameters
        ----------
        uploaded_files : List
            List of uploaded file objects to be processed and ingested.

        Raises
        ------
        CustomException
            If any error occurs during the ingestion process.
        """
        try:
            documents: List[Document] = self.load_documents(uploaded_files)
            if not documents:
                print("No valid documents found.")
                return
            self.store_in_vector_db(documents)
        except Exception as e:
            raise CustomException(e, sys)

if __name__ == '__main__':
    pass