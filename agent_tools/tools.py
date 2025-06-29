import sys

sys.path.append("../")

import os
from typing import Any
from langchain.tools import tool
from langchain_community.tools.polygon.financials import PolygonFinancials
from langchain_community.utilities.polygon import PolygonAPIWrapper
from langchain_community.tools.bing_search import BingSearchResults
from data_models.models import RagToolSchema
from langchain_pinecone import PineconeVectorStore
from utils.model_loader import ModelLoader
from utils.config_loader import load_config
from dotenv import load_dotenv
from pinecone import Pinecone
from langchain_tavily import TavilySearch

load_dotenv()
polygon_api_wrapper: PolygonAPIWrapper = PolygonAPIWrapper()
model_loader: ModelLoader = ModelLoader()
config: dict = load_config()


@tool(args_schema=RagToolSchema)
def retriever_tool(question: str) -> Any:
    """
    Retrieve relevant documents from the Pinecone vector store based on the input question.

    This tool uses the configured embedding model and Pinecone index to search for documents
    most similar to the user's query. The search is performed using a similarity score threshold
    and returns the top-k most relevant results.

    Parameters
    ----------
    question : str
        The query or question to retrieve relevant documents for.

    Returns
    -------
    Any
        The retrieval results from the vector store, typically a list of relevant documents.
    """
    pinecone_api_key: str = os.getenv("PINECONE_API_KEY")
    pc: Pinecone = Pinecone(api_key=pinecone_api_key)

    model_provider: str = config["model_provider"]["provider"]

    if model_provider == "azure":
        index_name: str = config["vector_db"]["azure"]["index_name"]

    elif model_provider == "groq":
        index_name: str = config["vector_db"]["groq"]["index_name"]

    elif model_provider == "google":
        index_name: str = config["vector_db"]["google"]["index_name"]

    vector_store: PineconeVectorStore = PineconeVectorStore(
        index=pc.Index(index_name),
        embedding=model_loader.load_embeddings(),
    )
    retriever = vector_store.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={
            "k": config["retriever"]["top_k"],
            "score_threshold": config["retriever"]["score_threshold"],
        },
    )
    retriever_result: Any = retriever.invoke(question)
    return retriever_result


tavilytool: TavilySearch = TavilySearch(
    max_results=config["tools"]["tavily"]["max_results"],
    search_depth="advanced",
    include_answer=True,
    include_raw_content=True,
)

financials_tool: PolygonFinancials = PolygonFinancials(api_wrapper=polygon_api_wrapper)
