from pydantic import BaseModel, Field
from langgraph.graph.message import add_messages
from typing import Annotated, TypedDict, List

class RagToolSchema(BaseModel):
    """
    Schema for RAG tool input.
    """
    question: str = Field(..., description="The question to retrieve relevant documents for.")

class QuestionRequest(BaseModel):
    """
    Schema for question request payload.
    """
    question: str = Field(..., description="The user's question.")

class ConversationState(TypedDict):
    """
    TypedDict for conversation state, used in workflow graphs.
    """
    messages: Annotated[List[str], add_messages]