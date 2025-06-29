from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages
from langgraph.prebuilt.tool_node import ToolNode, tools_condition
# from langchain_core.messages import AIMessage, HumanMessage
from typing_extensions import Annotated, TypedDict
from utils.model_loader import ModelLoader
from agent_tools.tools import retriever_tool, financials_tool, tavilytool
from typing import Any, Dict, Optional

class State(TypedDict):
    """
    Represents the state for the workflow graph.
    """
    messages: Annotated[list, add_messages]

class GraphBuilder:
    """
    Builds and manages a conversational workflow graph with LLM and tools integration.
    """

    def __init__(self) -> None:
        """
        Initializes the GraphBuilder with LLM, tools, and prepares for graph construction.
        """
        self.model_loader: ModelLoader = ModelLoader()
        self.llm: Any = self.model_loader.load_llm()
        self.tools: list = [retriever_tool, financials_tool, tavilytool]
        self.llm_with_tools: Any = self.llm.bind_tools(tools=self.tools)
        self.graph: Optional[Any] = None

    def _chatbot_node(self, state: State) -> Dict[str, list]:
        """
        Node function for chatbot: invokes the LLM with tools on the current state messages.

        Parameters
        ----------
        state : State
            The current state containing the conversation messages.

        Returns
        -------
        dict
            A dictionary with updated messages after LLM invocation.
        """
        return {"messages": [self.llm_with_tools.invoke(state["messages"])]}

    def build(self) -> None:
        """
        Builds and compiles the workflow graph with chatbot and tool nodes.
        """
        graph_builder: StateGraph = StateGraph(State)
        graph_builder.add_node("chatbot", self._chatbot_node)
        tool_node: ToolNode = ToolNode(tools=self.tools)
        
        graph_builder.add_node("tools", tool_node)
        graph_builder.add_conditional_edges("chatbot", tools_condition)
        graph_builder.add_edge("tools", "chatbot")
        graph_builder.add_edge(START, "chatbot")

        self.graph = graph_builder.compile()

    def get_graph(self) -> Any:
        """
        Returns the compiled workflow graph.

        Returns
        -------
        Any
            The compiled workflow graph.

        Raises
        ------
        ValueError
            If the graph has not been built yet.
        """
        if self.graph is None:
            raise ValueError("Graph not built. Call build() first.")
        return self.graph